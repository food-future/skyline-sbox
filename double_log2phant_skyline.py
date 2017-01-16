#!/usr/bin/python

import serial
import requests
import time
import json
import sys


#import logging
#logging.basicConfig(filename='./example.log',level=logging.DEBUG)


#### some basic variables


baseURL = 'http://159.203.128.53'
#baseURL = 'https://data.sparkfun.com'

publicKey_2='vZrrayEJzlipYLdGvPLJiqqlVO6v'
privateKey_2='r7eemMGdyAUwqjan8YjEFYYvZRQA'

publicKey_6='jkPmjaPoKztwAark4Wa9fDDqOgxj'
privateKey_6='wbrMA2rOWGu7m2l0vr2EUMMZ0zPE'

#serialPort="/dev/ttyACM0"	
serialPort="/dev/ttyUSB0"

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
            
            print 'raw serial input: ', line.strip()
          
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
                
                if devid=='6':


                    publicKey = publicKey_6
                    privateKey = privateKey_6
                    
                    temp_dht = str(p["data"]["temp_dht"])
                    humidity_dht = str(p["data"]["humidity_dht"])
                    
                    #print("here")
                    
                    temp_am2315 = str(p["data"]["temp_am2315"])
                    humidity_am2315 = str(p["data"]["humidity_am2315"])
                    #pressure_bme = str(p["data"]["pressure_bme"])
                    #altitude_bme = str(p["data"]["altitude_dht"])
                   
                

                    a1 = str(p["data"]["A1"])

                    a2 = str(p["data"]["A2"])
            
                    #a2 = str(p["data"]["A2"])

                    #a3 = str(p["data"]["A3"])

                    #a4 = str(p["data"]["A4"])

                    #a5 = str(p["data"]["A5"])

                    #print devid,rssi

                    #print temp, humidity, a0, a1, a2, a3, a4, a5

                    pushUrl = baseURL+'/input/'+str(publicKey)+'?private_key='+str(privateKey)+'&temp_dht='+temp_dht+'&humidity_dht='+humidity_dht+'&packetnum='+packetnum+'&rssi='+rssi+'&a1='+a1+'&a2='+a2+'&temp_am2315='+temp_am2315+'&humidity_am2315='+humidity_am2315
                         
                    print pushUrl

                    push = requests.get(pushUrl)
                    
                    print push
                
                elif devid=='2':

                    publicKey = publicKey_2
                    privateKey = privateKey_2
                    
                    temp_sht = str(p["data"]["temp_sht"])
                    humidity_sht = str(p["data"]["humidity_sht"])

                    battery_voltage=str(p["data"]["battery_voltage"])
                    
                    a0 = str(p["data"]["A0"])

                    a1 = str(p["data"]["A1"])
            
                    #a2 = str(p["data"]["A2"])

                    #a3 = str(p["data"]["A3"])

                    #a4 = str(p["data"]["A4"])

                    #a5 = str(p["data"]["A5"])

                    #print devid,rssi

                    #print temp, humidity, a0, a1, a2, a3, a4, a5

                    pushUrl = baseURL+'/input/'+str(publicKey)+'?private_key='+str(privateKey)+'&temp_sht='+temp_sht+'&humidity_sht='+humidity_sht+'&packetnum='+packetnum+'&rssi='+rssi+'&a0='+a0+'&a1='+a1+'&battery_voltage='+battery_voltage
                         
                    print pushUrl

                    push = requests.get(pushUrl)
                    
                    print push
                    
                    
                    
    except:

        error=sys.exc_info()[0]
        print("Unexpected error:", sys.exc_info()[0])
        #logging.debug(error)
     
        
        time.sleep(2)
        
