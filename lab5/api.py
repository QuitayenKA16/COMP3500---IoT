# ---------------- #
# Karamel Quitayen #
# COMP.3500 IoT    #
# Lab 5            #
# API Code         #
# ---------------- #

# necessary libraries 
from influxdb import InfluxDBClient
from flask import Flask, request, json
from flask_restful import Resource, Api
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# ------------ GLOBAL VARIABLES INIT ------------- #

broker_address = "192.168.0.19"
            
    
# --------------- Flask API Calls ---------------- #

class Led(Resource):

    # sets state of led on pi
    def post(self):
        # get json
        value = request.get_data()
        value = json.loads(value)
        print("post" + str(value))
        
        # if json is to talk to pi
        if value['device'] == "pi":
            print("rpi -> " , value['state'])
            client.publish("/rpi", value['state'])
                
        # if json is to talk to arduino
        else:
            print("arduino -> ", value['state'])
            client.publish("/arduino", value['state'])
    

    # returns avg light value over last 10 sec
    def get(self):
        # database query to get mean of vals from last 10 seconds
        query = 'select mean("value") from "light" where "time" > now()-10s'
        
        # make query
        result = dbclient.query(query)
        
        # get value inside result
        mean = list(result.get_points(measurement='light'))[0]['mean']
        return {'avg':mean}


# ------- SET UP MQTT, Influx, and Flask ------- #

client = mqtt.Client()
client.connect(broker_address)
dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')

app = Flask(__name__)
api = Api(app)
api.add_resource(Led, '/led')
app.run(host='0.0.0.0', debug=True)
