import time
import requests
import math
import random
import RPi.GPIO as GPIO


TOKEN = "BBFF-kgTpiBzSzrcqDyA95LDxlntQK86Zcs"  # Put your TOKEN here
DEVICE_LABEL = "sic-assgn-week10"  # Put your device label here 
VARIABLE_LABEL_1 = "Position"  # Put your first variable label here
VARIABLE_LABEL_2 = "Distance"  # Put your second variable label here


def build_payload(variable_1, variable_2):
    # Creates two random values for sending data
    value_1 = dist
    value_2 = value_1

    # Creates a random gps coordinates
    lat = random.randrange(34, 36, 1) + \
        random.randrange(1, 1000, 1) / 1000.0
    lng = random.randrange(-83, -87, -1) + \
        random.randrange(1, 1000, 1) / 1000.0
    payload = {variable_1: value_1,
               variable_2: value_2}
    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 21
GPIO_ECHO = 20
GPIO_LED = 18
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_LED, GPIO.OUT)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
	        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2 
    return distance



def main():
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")



if _name_ == '_main_':
    while (True):
            dist = distance()
            print ("jarak = %.1f cm" % dist)
            time.sleep(0.5)

            main()
            time.sleep(1)
