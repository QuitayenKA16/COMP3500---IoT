# ---------------- #
# Karamel Quitayen #
# COMP.3500 IoT    #
# Lab 2            #
# ---------------- #

# libraries necessary to access pins
import RPi.GPIO as GPIO
import time

# LED and button pin numbers
LED = 23
BUTTON = 18

# flags to keep track of button/LED state
light = GPIO.LOW
prevState = GPIO.LOW

# setup board
GPIO.setmode(GPIO.BCM)

# set LED as output
GPIO.setup(LED, GPIO.OUT)

# set BUTTON as input
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# endless loop
while True:

    # read button state
    currState = GPIO.input(BUTTON)
    
    # if button toggled
    if (currState == GPIO.HIGH and prevState == GPIO.LOW):
        if (ledState == GPIO.LOW):
            ledState = GPIO.HIGH
        else:
            ledState = GPIO.LOW
          
    # set button state (on or off) based on above logic
    GPIO.output(LED, ledState)
    
    # update previous state
    prevState = currState
