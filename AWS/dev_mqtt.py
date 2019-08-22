from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
	
host = 'a1wlltnsvntckz-ats.iot.ap-south-1.amazonaws.com'
rootCAPath = 'root-CA.pem'
certificatePath = '1e5e1bc664-certificate.pem.crt'
privateKeyPath = '1e5e1bc664-private.pem.key'
port = 8883 # When no port override for non-WebSocket, default to 8883
#port = 443 # When no port override for WebSocket, default to 443
useWebsocket = False
clientId = 'chargebuddy'
topic = 'pub'
mess='UzC'
mode='subscribe'
mode='publish'

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
while True:
	if mode=='subscribe':
		myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
	time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    if mode=='publish':
        message = {}
        message['message'] = mess
        message['sequence'] = loopCount
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish(topic, messageJson, 1)
        if mode == 'publish':
            print('Published topic %s: %s\n' % (topic, messageJson))
        loopCount += 1
    time.sleep(1)

