from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json


#Remove When uploaded in raspi
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#Setup Lock pin
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

GPIO.setup(7, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

lockers = {1:{"green_light":17,"red_light":27,"pin":22}, 0:{"green_light":5,"red_light":6,"pin":13}, 2:{"green_light":16,"red_light":20,"pin":21}, 3:{"green_light":25,"red_light":8,"pin":7}}

for i in lockers:
   GPIO.output(lockers[i]["pin"],True)
#GPIO.output(lockers[1]["pin"],False)

def change_led(slot,phone_status):
    green_pin = lockers[slot]['green_light']
    red_pin = lockers[slot]['red_light']
    if phone_status == 'outside':
        GPIO.output(green_pin,True)
        GPIO.output(red_pin,False)
        print("Green LED = ",green_pin)
    elif phone_status == 'inside':     
        GPIO.output(red_pin,True)
        GPIO.output(green_pin,False)
        print("Red LED = ",red_pin)

def open_locker(slot):
    print('XXXXXXXXXXXXXXXXXXXXX')
    #Remove When uploaded in raspi
    loc = lockers[slot]['pin']
    GPIO.output(loc, False)
    #GPIO.output(17, False)
    print("Unlocked = ",loc)
    print('XXXXXXXXXXXXXXXXXXXXX')

def close_locker(slot):
    print('XXXXXXXXXXXXXXXXXXXXX')
    #Remove When uploaded in raspi
    loc = lockers[slot]['pin']
    GPIO.output(loc, True)
    #GPIO.output(17, True)
    print("Locked = ",loc)
    print('XXXXXXXXXXXXXXXXXXXX')

def customCallback(client, userdata, message):
    instruction = json.loads(message.payload)
    if instruction['error']:
        print('XXXXXXXXXXXXXXXXXXXXX')
        print(instruction['error_desc'])
        print('XXXXXXXXXXXXXXXXXXXXX')
    else:
        phone_status = instruction['phone_status']
        action = instruction['action']
        slot = instruction['slot']
        if action == "open":
            open_locker(slot)
        elif action == "close":
            close_locker(slot)
        change_led(slot,phone_status)

host = 'a1wlltnsvntckz-ats.iot.ap-south-1.amazonaws.com'
rootCAPath = '/home/pi/Desktop/dev1/root-CA.pem'
certificatePath = '/home/pi/Desktop/dev1/1e5e1bc664-certificate.pem.crt'
privateKeyPath = '/home/pi/Desktop/dev1/1e5e1bc664-private.pem.key'
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

print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
while True:
    pass
        

# mess_load = {"message": "from_server", "slot": 3, "error": False, "station_number": "1", "action": "open"}

# customCallback(True,True,mess_load)

