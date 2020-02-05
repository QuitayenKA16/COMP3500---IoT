# ---------------- #
# Karamel Quitayen #
# COMP.3500 IoT    #
# Lab 3            #
# ---------------- #

# libraries necessary to access pins
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

# ------------ GLOBAL VARIABLES INIT ------------- #

# LED and button pin numbers
LED = 23
BUTTON = 18

# flags to keep track of button/LED state
ledState = GPIO.LOW
prevState = "off"

# raspberry pi ip address
broker_address = "192.168.0.19"


# --------- SET UP RASPBERRY PI CIRCUIT ---------- #

# setup board
GPIO.setmode(GPIO.BCM)

# set LED as output
GPIO.setup(LED, GPIO.OUT)

# set BUTTON as input
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# -------- FUNCTION TO READ ARDUINO MESSAGE ------ #

def on_message(client, userdata, message):
    # print incoming message
    print(str(message.topic) + " " + str(message.payload))
    
    # --- TOGGLE LOGIC FROM ASSIGNMENT 2 --- #
    currState = str(message.payload)
    if (currState == "on" and prevState == "off"):
        if (ledState == GPIO.LOW):
            ledState = GPIO.HIGH
        else:
            ledState = GPIO.LOW
          
    GPIO.output(LED, ledState)
    prevState = currState
        
    

# ------------- SET UP MQTT CLIENT --------------- #

# create new client instance
client = mqtt.Client() 

# connect to broker
client.connect(broker_address)

# set on message function
client.on_message = on_message

# subscribe to topic
client.subscribe("/button")

# start client
client.loop_start()
    

# ---------------- ENDLESS LOOP ------------------ #

try:
    while True: # wait for ctrl-c
    
        # read current button state
        if (GPIO.input(BUTTON) == HIGH):
            # send message that button was toggled on
            client.publish("/button", "on")
        else:
            # send message that button was toggled off
            client.publisH("/button", "off")
        
        pass
        
except KeyboardInterrupt:
    pass
    
    
# stop client
client.loop_stop()
