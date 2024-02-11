#!/usr/bin/env python

import sys
import os
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from time import sleep

def setup_gpio_and_servo():
    # Set GPIO numbering mode
    GPIO.setmode(GPIO.BOARD)

    # Set pin 11 as an output, and set servo1 as pin 11 as PWM
    GPIO.setup(32, GPIO.OUT)
    servo1 = GPIO.PWM(32, 50)  # Note 11 is pin, 50 = 50Hz pulse

    # Start PWM running, but with value of 0 (pulse off)
    servo1.start(0)
    print("Waiting for 2 seconds")
    sleep(2)

    return servo1

def move_servo(servo, angle):
    duty = 2 + (angle / 18)
    servo.ChangeDutyCycle(duty)
    sleep(1)

def main():
    servo = setup_gpio_and_servo()

    try:
        while True:
            # Create an instance of the RFID reader
            reader = SimpleMFRC522()

            try:
                print("Waiting for RFID card...")
                id, text = reader.read()

                print("Card detected! Moving servo to 70 degrees.")
                move_servo(servo, 70)

                # Do something with the RFID card data (e.g., Spotify integration)

            except Exception as e:
                print(f"Error reading RFID card: {e}")
                print("Moving servo back to 0 degrees.")
                move_servo(servo, 0)

            finally:
                sleep(2)  # Add a delay to avoid rapid consecutive reads

    except KeyboardInterrupt:
        pass

    finally:
        # Clean up GPIO at the end
        servo.stop()
        GPIO.cleanup()
        print("Goodbye")

if __name__ == "__main__":
    main()
