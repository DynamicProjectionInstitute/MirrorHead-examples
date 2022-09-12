#!/usr/bin/env python3

# Simple TELEMETRY readout example for the Mirror Head.
# TELEMETRY output must be enabled on the Mirror Head and a MQTT broker
# must be set up.

# Copyright (c) 2022 by Dynamic Projection Institute GmbH
# Author: Martin Willner <mw@dynamicprojection.com>

broker_address="2.0.0.2" 
#
# For a real world test with test.mosquitto.org (91.121.93.94) set the MQTT Broker IP on the Mirror Head to the same as below. Make sure you also 
# set the gateway correct so the Mirror Head can access the internet.
# Send: mosquitto_pub -h 91.121.93.94 -t "DPI/MH/global/input" -m "64 0 64 0 0 0 0 0 0 255 0 0 255 0 1", this will move the mirror and set the LED to blue. 
# To regain ArtNet/Web/DMX controll set the last byte to 0:
# mosquitto_pub -h 91.121.93.94 -t "DPI/MH/global/input" -m "64 0 64 0 0 0 0 0 0 255 0 0 255 0 0"
# 
# ENABLE THIS FOR INERNET TEST:
# broker_address="91.121.93.94" 


import paho.mqtt.client as mqtt 
import struct
co=0

def process_data(c,u,m):
    global co
    try:
        co+=1
        # telemetry status structure from the MH is in the form:
        # struct  __attribute__((__packed__)) telemetry_ {
        # uint32_t axis_position[2]; // Target position in AXIS units
        # uint32_t dmx_position[2]; // Target DMX position 
        # uint32_t tmc_step[2]; // Actual position of the motors in AXSIS units
        # uint8_t angles[2]; // selected PAN and TILT max. angle
        # }
        x=struct.unpack('IIIIIIBB',m.payload)
        print(m.topic,x) # simple output
        #print(co,x[0]," ",x[4]," ",x[1]," ",x[5]) # use this for plotting 
    except Exception as  err:
        print("error", err)


client = mqtt.Client("myuniq-id") 
client.on_message = process_data
client.connect(broker_address) 
client.subscribe("DPI/MH/#")
client.loop_forever()
