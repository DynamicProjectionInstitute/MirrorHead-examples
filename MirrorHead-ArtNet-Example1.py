#!/usr/bin/env python3

# Sending Art-Net(TM) DMX512 to the Mirror Head unit 
# Most simple version to send Art-Net DMX512
#
# Copyright (c) 2016,2017 by Dynamic Projection Institute GmbH, Vienna, Austria
# Author:  Martin Willner <willner@dynamicprojection.com>

import sys, socket, math, time, random
from ctypes import *

MIRROR_HEAD_IP="2.0.0.3"
		
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

    S = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    D = ArtNetDMX512()
    print("Random psition only on the high bytes (DMX#1 and DMX#3)")
    D.payload[0]=random.randint(0,255)
    D.payload[2]=random.randint(0,255)
    S.sendto(D, (MIRROR_HEAD_IP, ArtNetDMX512.PORT))



if __name__ == "__main__":
    print("*********** HIT CTRL+C TO EXIT THE DEMO AT ANY TIME ************")
    print("*** Mirror Head IP by configuration: "+str(MIRROR_HEAD_IP))
    main()

