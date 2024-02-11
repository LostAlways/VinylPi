#!/usr/bin/env python

import sys
import os
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from time import sleep
import time
from servo_control import setup_gpio_and_servo, move_servo
from stepper_control import setup_stepper_motor, rotate_stepper_motor, cleanup_stepper

def main():
    servo = setup_gpio_and_servo()
    motor_params = setup_stepper_motor()

    try:
        while True:
            reader = SimpleMFRC522()

            try:
                print("Waiting for RFID card...")
                id, text = reader.read()

                print("Card detected! Moving servo to 70 degrees.")
                move_servo(servo, 70)

                print("Rotating stepper motor continuously.")
                rotate_stepper_motor(*motor_params)

                # Do something with the RFID card data (e.g., Spotify integration)

            except Exception as e:
                print(f"Error reading RFID card: {e}")
                print("Moving servo back to 0 degrees.")
                move_servo(servo, 0)
                # Stop the stepper motor rotation
                cleanup_stepper()

            finally:
                sleep(2)

    except KeyboardInterrupt:
        pass

    finally:
        servo.stop()
        GPIO.cleanup()
        print("Goodbye")

if __name__ == "__main__":
    main()
