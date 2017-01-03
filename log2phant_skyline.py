#!/usr/bin/python

import serial
import requests
import time
import json
import sys


import logging
logging.basicConfig(filename='./example.log',level=logging.DEBUG)


#### some basic variables


baseURL = 'http://159.203.128.53'
#baseURL = 'https://data.sparkfun.com'

publicKey='MM34dG0vpWs6a9dy0gQaCz8gGVe'
privateKey='Ey7GjAzeYKsGX67Aq0BXhYKzdMn'

serialPort="/dev/ttyACM0"
#serialPort="/dev/ttyUSB1"

serialBaud = 9600

#loopDelay = 10 #seconds

endl="\n"

###### open and flush serial port

iteration = 0

while True:

    try:

        ser = serial.Serial(serialPort, serialBaud)

        #print "Waiting for serial port ..."
        time.sleep(3)
        #ser.flush() # flush to get rid of extraneous char

        #print "\n"

        ###### main loop 

        while True:

            #cmd = "READ"
            #cmd = cmd.strip() + endl
            #ser.write(cmd.encode())
            #print "Waiting for serial port ..."
            
            line = ser.readline()
            line=line.decode('utf-8')
            
            #print 'raw serial input: ', line.strip()
          
            parsed = line.split('\t')
            #parsed = "test"

            #print parsed[0]

            if len(parsed) ==2:

	        rssi=parsed[0].split(':')[1]

	        #print parsed[1]

	        j = str(parsed[1])

	        p = json.loads(j)
	

	        devid = str(p["id"])

	        packetnum = str(p["packetnum"])
	
	        rssi= int(rssi)

	        rssi = str(rssi)

                temp = str(p["data"]["temp"])
	
	        humidity = str(p["data"]["humidity"])

	        a0 = str(p["data"]["A0"])

	        a1 = str(p["data"]["A1"])
	
	        a2 = str(p["data"]["A2"])

	        a3 = str(p["data"]["A3"])

	        a4 = str(p["data"]["A4"])

	        a5 = str(p["data"]["A5"])

	        #print devid,rssi

	        #print temp, humidity, a0, a1, a2, a3, a4, a5

	        pushUrl = baseURL+'/input/'+str(publicKey)+'?private_key='+str(privateKey)+'&devid='+devid+'&temp='+temp+'&humidity='+humidity+'&packetnum='+packetnum+'&rssi='+rssi+'&a0='+a0+'&a1='+a1+'&a2='+a2+'&a3='+a3+'&a4='+a4+'&a5='+a5
                 
                print pushUrl

	        push = requests.get(pushUrl)
                
                print push
                
    except:

        error=sys.exc_info()[0]
        print("Unexpected error:", sys.exc_info()[0])
        logging.debug(error)
     
        
        time.sleep(2)
        
