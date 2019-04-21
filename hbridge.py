#!/usr/bin/pthon3
import gpiozero

pin_hb_ena = 18
pin_hb_in1 = 20
pin_hb_in2 = 21

ena = gpiozero.PWMLED(pin_hb_ena)
in1 = gpiozero.LED(pin_hb_in1)
in2 = gpiozero.LED(pin_hb_in2)
#ena = gpiozero.LED(pin_hb_ena)
#ena.on()

def set_throttle(percentvalue):
    global ena
    #print(percentvalue /100)
    ena.value = ( percentvalue / 100 )
    if percentvalue == 0:
        motor_off()

def motor_off():
    global in1, in2
    in1.off()
    in2.off()
    
def motor_forward():
    global in1, in2
    in1.on()
    in2.off()

def motor_reverse():
    global in1, in2
    in1.off()
    in2.on()
