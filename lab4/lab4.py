# ---------------- #
# Karamel Quitayen #
# COMP.3500 IoT    #
# Lab 4            #
# ---------------- #

# necessary libraries 
from influxdb import InfluxDBClient
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


# -------- FUNCTION TO READ ARDUINO MESSAGE ------ #

def on_message(client, userdata, message):
    valStr = message.payload.decode('ascii')
    receiveTime = datetime.datetime.utcnow()
    #print("ARDUINO -> PI : " + valStr)

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
    

# ------------- SET UP MQTT and Influx CLIENT --------------- #

# set up client for InfluxDB
dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')

# create new client instance
client = mqtt.Client() 
# connect to broker
client.connect(broker_address)
# set on message function
client.on_message = on_message
# subscribe to topic
client.subscribe("/sensor")
# start client
client.loop_start()
    

# ---------------- ENDLESS LOOP ------------------ #

try:
    while True: # wait for ctrl-c
        # database query
        query = 'select mean("value") from "light" where "time" > now()-10s'
        
        # make query
        result = dbclient.query(query)
        
        # get value inside result
        try:
            mean = list(result.get_points(measurement='light'))[0]['mean']
            print(mean)
            
            # if mean < 200, turn led on
            if (mean < 200):
                GPIO.output(LED, GPIO.HIGH)
                # else turn led off
            else:
                GPIO.output(LED, GPIO.LOW)

        except:
            pass
        

except KeyboardInterrupt:
    pass
    
    
# stop client
client.loop_stop()
