# ---------------- #
# Karamel Quitayen #
# COMP.3500 IoT    #
# Lab 5            #
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
    
# --------------- Flask API Calls ---------------- #

class DeviceState(Resource):

    # sets state of led on pi
    def post(self):
        # get json
        value = request.get_data()
        value = json.loads(value)
        
        # if json is to talk to pi
        if value['device'] == "pi":
            if value['state'] == "on":
                GPIO.output(LED, GPIO.HIGH)
            else:
                GPIO.output(LED, GPIO.LOW)
                
        # if json is to talk to arduino
        else:
            client.publish("/arduino", value['state'])
    

    # returns avg light value over last 10 seconds
    def get(self):
        # database query to get mean of vals from last 10 seconds
        query = 'select mean("value") from "light" where "time" > now()-10s'
        
        # make query
        result = dbclient.query(query)
        
        # get value inside result
        mean = list(result.get_points(measurement='light'))[0]['mean']
        return {'avg':str(mean)}


# ------- SET UP MQTT, Influx, and Flask --------- #

# set up client for InfluxDB
dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')

# set up Flask
app = Flask(__name__)
api = Api(app)
api.add_resource(HelloWorld, '/test')
app.run(host='0.0.0.0', debug=True)

# create new MQTT client instance
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

except KeyboardInterrupt:
    pass
    
    
# stop client
client.loop_stop()
