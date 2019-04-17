#!/usr/bin/python3
import os, time
import rovercom

thisfilepath = os.path.dirname(__file__)

# Global Autopilot bool:
autopilot = False

# steering var:
# 0 = steering left
# 1 = steering center
# 2 = steering right
steering = 0 # (stopped)

# throttle var:
# range of 0 (stopped) to 10 (full throttle)
throttle = 0

status = rovercom.status_fifo()

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
    global steering
    global throttle
    
    lcmd = cmd.lower()
    args = cmd.split()
    largs = lcmd.split()
    
    # logic for processing commands (add new ones here):
    if lcmd == 'quit':
        exit()

    if lcmd == 'stop':
        print('stop')
        # stop resets steering and sets throttle to zero:
        steering = 1
        throttle = 0
        return

    if largs[0] == 'move':
        if len(args) > 1:
            if largs[1] == 'left':
                print('move left')
                throttle = 2
                steering = 0
            elif largs[1] == 'forward':
                print('move forward')
                throttle = 5
                steering = 1
            elif largs[1] == 'right':
                print('move right')
                throttle = 2
                steering = 2
        return
    
    if largs[0] == 'steer':
        if len(args) > 1:
            if largs[1] == 'left':
                print('steer left')
                steering = 0
            elif largs[1] == 'center':
                print('steer center')
                steering = 1
            elif largs[1] == 'right':
                print('steer right')
                steering = 2
        return
    
    if largs[0] == 'throttle':
        if len(args) > 1:
            print('Setting throttle to ' + args[1])
            throttle = int(args[1])
        return

def do_init():
    # TODO:
    # init ultrasonic range sensor
    rovercom.init_fifos()
    print('Rover Daemon')
    print('Init complete.')

def mainloop():
    laststatus = None
    
    while (1):
        cmd = rovercom.checkforcommand()
        if cmd == '':
            time.sleep(.25)
        else:
            #print('Received command: ' + cmd)
            processcommand(cmd)

        if autopilot == True:
            vcmd = checkforvisioncommand()
            processcommand(vcmd)
        
        # build status
        curstatus = ''
        if steering == 0:
            curstatus = '<-  '
        elif steering == 1:
            curstatus = '^   '
        elif steering == 2:
            curstatus = '->  '
        
        curstatus += str(throttle * 10) + '%'
        
        if laststatus != curstatus:
            #print('updating status')
            status.setstatus(curstatus)
            laststatus = curstatus

if __name__ == '__main__':
    do_init()
    mainloop()
