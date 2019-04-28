#!/usr/bin/python3
import gpiozero

# steer_left = -1
# steer_left_deg = 0
# steer_center = 0
# steer_center_deg = 90
# steer_right = 1
# steer_center_deg = 180

# adjust steering trim here:
steering_trim = -.1

def set_steering_servo_val(servo, servoval):
    newval = -(servoval + steering_trim)
    if newval > 1:
        newval = 1
    if newval < -1:
        newval = -1
    servo.value = newval

def val_to_deg(sv):
    return (sv + 1) * 90

def deg_to_val(dv):
    return (dv / 90) - 1
