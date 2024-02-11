#!/usr/bin/env python

import sys
import os
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from time import sleep
import time

# ... (previous code)

def setup_stepper_motor():
    in1 = 4
    in2 = 17
    in3 = 27
    in4 = 22

    step_sleep = 0.002
    step_count = 4096
    direction = False
    step_sequence = [[1, 0, 0, 1],
                     [1, 0, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 1, 1, 0],
                     [0, 0, 1, 0],
                     [0, 0, 1, 1],
                     [0, 0, 0, 1]]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(in3, GPIO.OUT)
    GPIO.setup(in4, GPIO.OUT)

    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

    motor_pins = [in1, in2, in3, in4]
    motor_step_counter = 0

    return (motor_pins, step_sequence, motor_step_counter, step_sleep, direction, step_count)

def rotate_stepper_motor(motor_pins, step_sequence, motor_step_counter, step_sleep, direction, step_count):
    try:
        i = 0
        for i in range(step_count):
            for pin in range(0, len(motor_pins)):
                GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
            if direction == True:
                motor_step_counter = (motor_step_counter - 1) % 8
            elif direction == False:
                motor_step_counter = (motor_step_counter + 1) % 8
            else:  # defensive programming
                print("uh oh... direction should *always* be either True or False")
                cleanup()
                exit(1)
            time.sleep(step_sleep)

    except KeyboardInterrupt:
        cleanup()
        exit(1)

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
                cleanup()

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
