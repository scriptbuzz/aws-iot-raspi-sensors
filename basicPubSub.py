'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''
# Name: M Bitar
# Date: March 15, 2020
# Project: AWS IoT Sensor Node

from sense_hat import SenseHat
from time import sleep
from random import randint

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

sleep_val = .1
text_speed = .05
sense = SenseHat()
sense.clear()

r = 255
g = 255
b = 255

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)

sense.clear((0, 0, 0))
back_clr = (0, 0, 0)

GO=False
WARN=False
ALARM=False


sense.show_letter("A", red)
sleep(1)
sense.show_letter("W", red)
sleep(1)
sense.show_letter("S", red)
sleep(1)
#sense.show_message("AWS IoT Prototype", text_colour=red, back_colour=back_clr, scroll_speed=.05)


AllowedActions = ['both', 'publish', 'subscribe']

# Custom MQTT message callback
def customCallback(client, userdata, message):
    #print("Received a new command: ")
    global WARN,ALARM, GO
    print(message.payload)
    if "WARN" in message.payload:
        print("===== ATTENTION: EXECUTE STOP COMMMAND =====")
        WARN=True

    elif "ALARM" in message.payload:
        print("===== ATTENTION: EXECUTE ALARM COMMMAND =====") 
        ALARM=True 

    elif "GO" in message.payload:
        print("===== ATTENTION: EXECUTE GO COMMMAND =====")  
        GO=True

           
    #print("from topic: ")
    #print(message.topic)
    #print("--------------\n\n")


# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-p", "--port", action="store", dest="port", type=int, help="Port number override")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",
                    help="Operation modes: %s"%str(AllowedActions))
parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",
                    help="Message to publish")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
port = args.port
useWebsocket = args.useWebsocket
clientId = args.clientId
topic = args.topic

if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
    exit(2)

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Port defaults
if args.useWebsocket and not args.port:  # When no port override for WebSocket, default to 443
    port = 443
if not args.useWebsocket and not args.port:  # When no port override for non-WebSocket, default to 8883
    port = 8883

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
if args.mode == 'both' or args.mode == 'subscribe':
    myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    if GO:
        print("GGGGGGGGGGGGGGGGGGGGGGGGG")
        sense.clear(green)
        sleep(3)
        Go=False
    if ALARM:
        print("AAAAAAAAAAAAAAAAAAAAAAAA")
        sense.clear(red)
        sleep(3)
        ALARM=False 
    if WARN:
        print("WWWWWWWWWWWWWWWWWWWWWWWW")
        sense.clear(yellow)
        sleep(3)
        WARN=False               
    temp = sense.get_temperature()
    print("Temp: "+str(round(temp)))
    sense.show_message("T:"+str(round(temp)), text_colour=red, back_colour=back_clr, scroll_speed=text_speed)
    sense.clear((0, 0, 0))
    sleep(sleep_val )
    
    humidity = sense.get_humidity()
    print("Humidity: "+str(round(humidity)))
    sense.show_message("H:"+str(round(humidity)), text_colour=red, back_colour=back_clr, scroll_speed=text_speed)
    sleep(sleep_val )
    
    pressure = sense.get_pressure()
    print("Pressure: "+str(round(pressure)))
    sense.show_message("P:"+str(round(pressure)), text_colour=red, back_colour=back_clr, scroll_speed=text_speed)
    sense.clear((0, 0, 0))
    sleep(sleep_val )
    
    if args.mode == 'both' or args.mode == 'publish':
        message = {}
        message['message'] = "TEMP"
        message['sequence'] = str(round(temp))
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish(topic, messageJson, 1)
        if args.mode == 'publish':
            print('Published topic %s: %s\n' % (topic, messageJson))
        loopCount += 1
        
        message = {}
        message['message'] = "HUMIDITY"
        message['sequence'] = str(round(humidity))
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish(topic, messageJson, 1)
        if args.mode == 'publish':
            print('Published topic %s: %s\n' % (topic, messageJson))
        loopCount += 1
        
        message = {}
        message['message'] = "PRESSURE"
        message['sequence'] = str(round(pressure))
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish(topic, messageJson, 1)
        if args.mode == 'publish':
            print('Published topic %s: %s\n' % (topic, messageJson))
        loopCount += 1
        
    time.sleep(1)

