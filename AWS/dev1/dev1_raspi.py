from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

'''
#Remove When uploaded in raspi
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#Setup Lock pin
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
'''

def open_locker(slot):
    print('XXXXXXXXXXXXXXXXXXXXX')
    print(slot,"Unlocked")
    print('XXXXXXXXXXXXXXXXXXXXX')

def close_locker(slot):
    print('XXXXXXXXXXXXXXXXXXXXX')
    print(slot,"Locked")
    print('XXXXXXXXXXXXXXXXXXXXX')

def customCallback(client, userdata, message):
    instruction = json.loads(message.payload)
    action = instruction['action']
    slot = instruction['slot']
    if instruction['error']:
        print('XXXXXXXXXXXXXXXXXXXXX')
        print(instruction['error_desc'])
        print('XXXXXXXXXXXXXXXXXXXXX')
    else:
        if action == "open":
            open_locker(slot)
        elif action == "close":
            close_locker(slot)

host = 'a1wlltnsvntckz-ats.iot.ap-south-1.amazonaws.com'
rootCAPath = 'root-CA.pem'
certificatePath = '1e5e1bc664-certificate.pem.crt'
privateKeyPath = '1e5e1bc664-private.pem.key'
port = 8883 # When no port override for non-WebSocket, default to 8883
useWebsocket = False
clientId = 'dev1'
topic = 'dev1'
mess='from_dev1'

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
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 1, 2)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(5)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)


def publish_to_server():

#    status = get_status()
    message = {}
    message['message'] = "No Message yet"
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish('server', messageJson, 1)
    print('Published topic %s: %s\n' % ('server', messageJson))
    time.sleep(1)
    return True

while True:
	pass

# mess_load = {"message": "from_server", "slot": 3, "error": False, "station_number": "1", "action": "open"}

# customCallback(True,True,mess_load)

