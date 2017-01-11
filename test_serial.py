#!/usr/bin/python

import serial
import requests
import time
import json
import sys


#serialPort="/dev/ttyACM0"
serialPort="/dev/ttyUSB0"

serialBaud = 9600


while True:

    try:

        ser = serial.Serial(serialPort, serialBaud)

        time.sleep(3)


        while True:

          
            
            line = ser.readline()
            line=line.decode('utf-8')
            
            print 'raw serial input: ', line.strip()
                
    except:

        error=sys.exc_info()[0]
        print("Unexpected error:", sys.exc_info()[0])
     
        
        time.sleep(2)
        
