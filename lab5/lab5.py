# ---------------- #
# Karamel Quitayen #
# COMP.3500 IoT    #
# Lab 5            #
# Broker Code      #
# ---------------- #

# necessary libraries 
from influxdb import InfluxDBClient
from flask import Flask, request, json
from flask_restful import Resource, Api
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import datetime

# ------------ GLOBAL VARIABLES INIT ------------- #

# LED pin number
LED = 23

# raspberry pi ip address
broker_address = "192.168.0.19"


# --------- SET UP RASPBERRY PI CIRCUIT ---------- #

# setup board
GPIO.setmode(GPIO.BCM)

# set LED as output
GPIO.setup(LED, GPIO.OUT)


# --------- FUNCTION TO READ MQTT MESSAGE --------- #

def on_message(client, userdata, message):
    if message.topic == "/sensor":
        valStr = message.payload.decode('ascii')
        receiveTime = datetime.datetime.utcnow()
        print("ARDUINO -> PI : " + valStr)

        # create json to insert into db
        json_body = [{
            "measurement": 'light',
            "time": receiveTime,
            "fields": {
                "value": float(valStr)
            }
        }]
    
        # write to db
        dbclient.write_points(json_body)

    elif message.topic == "/rpi":
        if message.payload.decode('ascii') == "on":
            GPIO.output(LED, GPIO.HIGH)
        else:
            GPIO.output(LED, GPIO.LOW)

# ------------- SET UP MQTT, Influx ------------- #

# set up client for InfluxDB
dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')

# create new MQTT client instance
client = mqtt.Client() 
# connect to broker
client.connect(broker_address)
# set on message function
client.on_message = on_message
# subscribe to topic
client.subscribe("/sensor")
client.subscribe("/rpi")
# start client
client.loop_start()
    

# ---------------- ENDLESS LOOP ------------------ #

try:
    while True: # wait for ctrl-c
        pass

except KeyboardInterrupt:
    pass
    
    
# stop client
client.loop_stop()
GPIO.cleanup()
