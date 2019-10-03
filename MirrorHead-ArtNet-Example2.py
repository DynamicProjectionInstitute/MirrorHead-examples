#!/usr/bin/env python3
# Sending Art-Net(TM) DMX512 to the Mirror Head unit 
# This example shows how a 44Hz DMX512 can be done using threads.
#
# Copyright (c) 2016,2017 by Dynamic Projection Institute GmbH, Vienna, Austria
# Author:  Martin Willner <willner@dynamicprojection.com>

import sys, socket, math, time, random
from ctypes import *
from threading import Thread


MIRROR_HEAD_IP="2.0.0.3"

class DMX(Thread):
# DMX thread that send at a constant rate.
	def __init__ (self,ip):
		Thread.__init__(self)
		self.ip = ip
		self.status = -1
		self.packet = ArtNetDMX512()
		self.S = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	def run(self):
		while not exitthread:
			self.S.sendto(self.packet, (self.ip, ArtNetDMX512.PORT))
			time.sleep(1.0/44.0)
	
		
class ArtNetDMX512(LittleEndianStructure):
# Constructing the Art-Net DMX512 Packet at opcode 0x5000
# Art-Net specs see: http://artisticlicence.com/
    PORT = 0x1936
    _fields_ = [("id", c_char * 8),
                ("opcode", c_ushort),
                ("protverh", c_ubyte),
                ("protver", c_ubyte),
                ("sequence", c_ubyte),
                ("physical", c_ubyte),         
                ("universe", c_ushort),
                ("lengthhi", c_ubyte),
                ("length", c_ubyte),
                ("payload", c_ubyte * 512)]
    def __init__(self):
        self.id = b"Art-Net"
        self.opcode = 0x5000
        self.protver = 14
        self.universe = 0
        self.lengthhi = 2


def main():
	# Mirror Head Art-Net IP - default is: 2.0.0.4
	dmxthread = DMX(MIRROR_HEAD_IP) 
	dmxthread.start()


	POSMIN = 0
	POSMAX = 65535
	POSCENTER = int((POSMAX + 1) / 2)

	# We set all 512 DMX channels to make sure all have a value.  
	for i in range(0,len(dmxthread.packet.payload)):
		dmxthread.packet.payload[i]=0 


# This is the endless demonstration loop.
	while 1:
		time.sleep(4)
		print("*** GOTO CENTER POSITION - SNAP")
		mk_pos(dmxthread,POSCENTER,POSCENTER)

		time.sleep(4)
		print("*** GOTO MINIMUM POSITION - SNAP")
		mk_pos(dmxthread,POSMIN,POSMIN)

		time.sleep(4)
		print("*** GOTO MAXIMUM POSITION - SNAP")
		mk_pos(dmxthread,POSMAX,POSMAX)

		for i in range(1,5):
			time.sleep(4)
			print("*** GOTO RANDOM POSITION #"+str(i)+" - SNAP")
			mk_pos(dmxthread,random.randint(0,65535),random.randint(0,65535))
			print("*** SET RANDOM LED - SNAP")
			mk_led(dmxthread,random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))

		print("*** SWEEP LED in 5 sec")
		mk_led(dmxthread,0,255,255,255)

		for t in range(0,255):
			mk_led(dmxthread,t,255,255,255)
			time.sleep(5.0/255.0)			  

		for t in range(255,0,-1):
			mk_led(dmxthread,t,255,255,255)
			time.sleep(5.0/255.0)			  



def mk_pos(obj,p,t):
# Set the Art-Net DMX payload out of the 16bit pan and tilt values.
	pan_h,pan_l = split_to_low_high(p)
	tilt_h,tilt_l = split_to_low_high(t)
	print("PAN: "+str(p).zfill(5)+" TILT: "+str(t).zfill(5)+" => DMX #1:"+str(pan_h).zfill(3)+ " DMX #2:"+str(pan_l).zfill(3)+" DMX #3:"+str(tilt_h).zfill(3)+ " DMX #4:"+str(tilt_l).zfill(3))
	obj.packet.payload[0] = pan_h
	obj.packet.payload[1] = pan_l
	obj.packet.payload[2] = tilt_h
	obj.packet.payload[3] = tilt_l

def mk_led(obj,m,r,g,b):
	print("LED M:"+str(m).zfill(3)+" LED R:"+str(r).zfill(3)+" LED G:"+str(g).zfill(3)+" LED B:"+str(b).zfill(3))
	obj.packet.payload[9]=m
	obj.packet.payload[10]=r
	obj.packet.payload[11]=g
	obj.packet.payload[12]=b


def split_to_low_high(v):
# Helper function to split 16bit values into 2x 8bit for DMX.
	l = (v & 0xff)
	h= ((v >> 8) & 0xff )
	return h,l


if __name__ == "__main__":
	try:
		exitthread = False
		print("*********** HIT CTRL+C TO EXIT THE DEMO AT ANY TIME ************")
		print("*** Mirror Head IP by configuration: "+str(MIRROR_HEAD_IP))
		main()
	except KeyboardInterrupt:
		exitthread = True
		raise


