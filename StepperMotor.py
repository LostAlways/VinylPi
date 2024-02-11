#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

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

    return motor_pins, step_sequence, motor_step_counter, step_sleep, direction, step_count

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
                print("Uh oh... direction should *always* be either True or False")
                cleanup_stepper()
                exit(1)
            sleep(step_sleep)

    except KeyboardInterrupt:
        cleanup_stepper()
        exit(1)

def cleanup_stepper():
    GPIO.cleanup()
    print("Stepper motor cleanup completed.")
