#!/usr/bin/python3
import os, errno, time

# Global Autopilot bool:
autopilot = False

# steering var:
# 0 = steering left
# 1 = steering center
# 2 = steering right
steering = 0 (stopped)

# throttle var:
# range of 0 (stopped) to 10 (full throttle)

def checkforcommand():
    incmd = ''
    try:
        with os.open("/tmp/rover_cmd", os.O_RDONLY | os.O_NONBLOCK) as file:
            incmd = os.read(file, 200);
    except:
        pass
    
    return incmd

def checkforvisioncommand():
    
    # check for object in path of car:
    #obj_dist = get_ultrasonic_reading()
    obj_dist = 100
    if obj_dist <= 100 and obj_dist > 50:
        # slow down
        return 'throttle ' + str(3)
    elif obj_dist <= 50 and obj_dist > 25:
        # slow down more
        return 'throttle ' + str(1)
    elif obj_dist <= 25:
        # zero throttle (temp stop)
        return 'throttle ' + str(0)

    # TODO:
    # pull image frame from camera
    # process with artificial neural network
    # return command

    nn_result = 0

    if nn_result == [1,0,0,0]:
        return 'stop'
    elif nn_result == [0,1,0,0]:
        return 'move forward'
    elif nn_result == [0,0,1,0]:
        return 'move left'
    elif nn_result == [0,0,0,1]:
        return 'move right'

    # unexpected result from artificial neural network--return ''
    return ''

def processcommand(cmd):
    lcmd = cmd.lower()
    args = cmd.split()
    largs = lcmd.split()
    
    # logic for processing commands (add new ones here):
    if lcmd == 'quit':
        exit()

    if lcmd == 'stop':
        # stop resets steering and sets throttle to zero:
        steering = 1
        throttle = 0

    if largs[0] == 'move':
        if len(args) > 1:
            if larg[1] == 'left':
                throttle = 2
                steering = 0
            elif larg[1] == 'forward':
                throttle = 5
                steering = 1
            elif larg[1] == 'right':
                throttle = 2
                steering = 2

def do_init():
    # TODO:
    # init ultrasonic range sensor
    pass

def mainloop():
    
    while (1):
        cmd = checkforcommand()
        if cmd == '':
            sleep(.25)
        else:
            processcommand(cmd)

        if autopilot == True:
            vcmd = checkforvisioncommand()
            processcommand(vcmd)

if __name__ == '__main__':
    do_init()
    mainloop()
