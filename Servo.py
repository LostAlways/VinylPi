#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

def setup_gpio_and_servo():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(32, GPIO.OUT)
    servo1 = GPIO.PWM(32, 50)
    servo1.start(0)
    print("Waiting for 2 seconds")
    sleep(2)
    return servo1

def move_servo(servo, angle):
    duty = 2 + (angle / 18)
    servo.ChangeDutyCycle(duty)
    sleep(1)

def cleanup_servo(servo):
    servo.stop()
    GPIO.cleanup()
    print("Servo cleanup completed.")

