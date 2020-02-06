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
prevState = GPIO.LOW

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
    # received message from arduino to turn led on
    if ("on" in message.payload.decode('ascii')):
        print("ARDUINO -> PI : on")
        GPIO.output(LED, GPIO.HIGH)

    # received message from arduino to turn led off
    else:
        print("ARDUINO -> PI : off")
        GPIO.output(LED, GPIO.LOW)
        

# ------------- SET UP MQTT CLIENT --------------- #

# create new client instance
client = mqtt.Client() 

# connect to broker
client.connect(broker_address)

# set on message function
client.on_message = on_message

# subscribe to topic
client.subscribe("/piLED")

# start client
client.loop_start()
    

# ---------------- ENDLESS LOOP ------------------ #

try:
    while True: # wait for ctrl-c

        # --- TOGGLE LOGIC FROM ASSIGNMENT 2 --- #
        currState = GPIO.input(BUTTON)

        if (currState == GPIO.HIGH and prevState == GPIO.LOW):
            if (ledState == GPIO.LOW):
                ledState = GPIO.HIGH
                print("PI -> ARDUINO : on")
                # send message to arduino that button was toggled off
                client.publish("/arduinoLED", "on")
            else:
                ledState = GPIO.LOW
                print("PI -> ARDUINO : off")
                # send message to arduino that button was toggled off
                client.publish("/arduinoLED", "off")
                
        prevState = currState
            
                
except KeyboardInterrupt:
    pass
    
    
# stop client
client.loop_stop()
