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
buttonFlag = 0

# setup board
GPIO.setmode(GPIO.BCM)

# set LED as output
GPIO.setup(LED, GPIO.OUT)

# set BUTTON as input
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# endless loop
while True:

    # check button state
    buttonClicked = GPIO.input(BUTTON)

    # wait for button to be clicked
    while (buttonClicked != 1):
        # check to see if button was clicked
        buttonClicked = GPIO.input(BUTTON)

        #if button clicked and LED is off
        if (buttonClicked == 1 and buttonFlag == 0):
            # turn on LED
            GPIO.output(LED, GPIO.HIGH)
            # update flag
            buttonFlag = 1

        #if button clicked and LED is on
        elif (buttonClicked == 1 and buttonFlag == 1):
            # turn off LED
            GPIO.output(LED, GPIO.LOW)
            # update flag
            buttonFlag = 0

        while (buttonClicked == 1):
            buttonClicked = GPIO.input(BUTTON)
