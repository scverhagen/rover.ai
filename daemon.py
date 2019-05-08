#!/usr/bin/python3
import os, time
import warnings
import evdev
import gpiozero

import rovercom
import hbridge
import servo

global hasvision
hasvision = False


import vision
thisfilepath = os.path.dirname(__file__)

# Global Autopilot bool:
autopilot = False

# steering var:
# -1 = steering left
# 0 = steering center
# 1 = steering right
steering = 0 # (center)
laststeering = 0 # used to detect steering changes
steering_servo = gpiozero.Servo(27)

# throttle var:
# full throttle in reverse = -100
# stopped = 0
# full throttle forwards = 100
throttle = 0

hasDistanceSensor = False
distance_sensor = None
obj_dist = -1
#try:
distance_sensor = gpiozero.DistanceSensor(echo=17, trigger=4, max_distance=4, partial=True)
for x in range(1, 8):
    print(distance_sensor.distance)
    time.sleep(1)
    if int(distance_sensor.distance * 100) > 0:
        print('Distance sensor activated.')
        hasDistanceSensor = True
        break
#except:
#    hasDistanceSensor = False
#    print('No distance sensor found.  Disabling ultrasonic features...')

hasGameController = False
game_controller = None
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for thisdev in devices:
    if 'gamepad' in lower(device.name):
        game_controller = evdev.InputDevice(thisdev.fn)
        hasGameController = True

start_time = time.time()
status = rovercom.status_fifo()

def checkforvisioncommand():
    
    # 0 forward
    # 1 left
    # 2 right

    nn_result = vision.get_next_decision()

    if nn_result == 0:
        return 'steer center'
    elif nn_result == 1:
        return 'steer left'
    elif nn_result == 2:
        return 'steer right'

    # unexpected result from artificial neural network--return ''
    return ''

def checkgamepad():
    global game_controller
    ev = game_controller.read_one()

    # no event in queue:
    if ev == None:
        return None

    # debug for now:
    print('New bluetooth game controller event:')
    print('Type' + str(ev.type))
    print('Code' + str(ev.code))
    print('Value' + str(ev.value))

    key = ''
    if key == 'up':
        return 'move forward'

    if key == 'down':
        return 'move backwards'

    if key == 'up left':
        c = []
        c.append('move forward')
        c.append('steer left')
        return c

    if key == 'up right':
        c = []
        c.append('move forward')
        c.append('steer right')
        return c

    if key == 'down left':
        c = []
        c.append('move backwards')
        c.append('steer left')
        return c

    if key == 'down right':
        c = []
        c.append('move backwards')
        c.append('steer right')
        return c

def checkultrasonic():
    global start_time
    global hasDistanceSensor
    global throttle
    global obj_dist
   
    if (time.time() - start_time) < 1:
        return

    if hasDistanceSensor == True:
        obj_dist = round(distance_sensor.distance * 100)
        #print(obj_dist)
    else:
        obj_dist = 400
        
    start_time = time.time()
    
    if obj_dist <= 200 and obj_dist > 100:
        # slow down
        if throttle > 85:
            return 'throttle ' + str(85)
    elif obj_dist <= 100 and obj_dist > 75:
        # slow down more
        if throttle > 75:
            return 'throttle ' + str(75)
    elif obj_dist <= 75 and obj_dist > 50:
        # crawl
        if throttle > 60:
            return 'throttle ' + str(60)
    elif obj_dist <= 50:
        # zero throttle (temp stop)
        return 'throttle ' + str(0)

    return None

def processacommand(cmd):
    global throttle, steering, hasDistanceSensor, autopilot
    lcmd = cmd.lower()
    args = cmd.split()
    largs = lcmd.split()
    
    # logic for processing commands (add new ones here):
    if lcmd == 'quit':
        exit()

    if lcmd == 'poweroff':
        print('Powering off--good bye!')
        os.system('poweroff')

    if lcmd == 'stop':
        print('stop')
        # stop resets steering and sets throttle to zero:
        steering = 0
        throttle = 0
        return

    if lcmd == 'hard stop':
        # emergency stop
        c = []
        c.append('throttle -75')
        c.append('wait 1')
        c.append('stop')
        processcommand(c)
    
    if largs[0] == 'wait':
        if len(args) > 1:
            time.sleep(args[1])
        else:
            time.sleep(1)

    if largs[0] == 'move':
        if len(args) > 1:
            if largs[1] == 'left':
                print('move left')
                throttle = 75
                steering = -1
            elif largs[1] == 'forward':
                print('move forward')
                throttle = 100
                #steering = 0
            elif largs[1] == 'right':
                print('move right')
                throttle = 75
                steering = 1
            elif largs[1] == 'backwards':
                print('move backwards')
                throttle = -100
                #steering = 0
        return

    if largs[0] == 'steerval':
        if len(args) > 1:
            print('steerval ' + args[1])
            steering = int(args[1])

    if largs[0] == 'steerdeg':
        if len(args) > 1:
            print('steerdeg ' + args[1])
            steering = servo.deg_to_val(int(args[1]))

    if largs[0] == 'steer':
        if len(args) > 1:
            if largs[1] == 'left':
                print('steer left')
                steering = -1
            elif largs[1] == 'center':
                print('steer center')
                steering = 0
            elif largs[1] == 'right':
                print('steer right')
                steering = 1
        return
    
    if largs[0] == 'throttle':
        if len(args) > 1:
            print('Setting throttle to ' + args[1])
            throttle = int(args[1])
        return

    if largs[0] == 'disable':
        if largs[1] == 'distancesensor':
            print('distance sensor disabled')
            hasDistanceSensor = False

    if largs[0] == 'slow':
        if largs[1] == 'down':
            throttle = throttle - 10
            if throttle < 0:
                throttle = 0

    if largs[0] == 'speed':
        if largs[1] == 'up':
            throttle = throttle + 10
            if throttle > 100:
                throttle = 100

    if largs[0] == 'increase':
        if largs[1] == 'throttle':
            throttle = throttle + 10
            if throttle > 100:
                throttle = 100
                
    if largs[0] == 'decrease':
        if largs[1] == 'throttle':
            throttle = throttle - 10
            if throttle < -100:
                throttle = -100

    if largs[0] == 'autopilot':
        if largs[1] == 'on':
            autopilot == True
            print('autopilot on')
        elif largs[1] == 'off':
            autopilot == False
            print('autopilot off')

def processcommand(cmd):
    if cmd == None:
         return

    cmds = []
    if isinstance(cmd, str):
        cmds.append(cmd)
        
    for thiscmd in cmds:
        processacommand(thiscmd)

def do_init():
    rovercom.init_fifos()
    print('Rover Daemon')
    hbridge.motor_off()
    hbridge.set_throttle(0)
    print('Init complete.')

def mainloop():
    global hasDistanceSensor, obj_dist, throttle, steering, laststeering, autopilot
    laststatus = None
   
    while (1):

        cmd = rovercom.checkforcommand()
        if cmd == '':
            time.sleep(.25)
        else:
            #print('Received command: ' + cmd)
            processcommand(cmd)

        # check distance senor (if equipped)
        if hasDistanceSensor == True:
            processcommand( checkultrasonic() )

        # game controller (if equipped)
        if hasGameController == True:
            processcommand( checkgamepad() )

        if autopilot == True:
            vcmd = checkforvisioncommand()
            processcommand(vcmd)

        # control motor:
        hbridge.set_throttle(throttle)

        # set steering:
        if steering != laststeering:
            servo.set_steering_servo_val(steering_servo, steering)
            laststeering = steering
        
        # build status
        curstatus = ''
        c90 = round(steering)
        if c90 == -1:
            curstatus = '<-  '
        elif c90 == 0:
            if throttle < 0:
                curstatus = '\/  '
            elif throttle > 0:
                curstatus = '/\   '
        elif c90 == 1:
            curstatus = '->  '

        curstatus += 's_' + str(throttle) + '%'
        curstatus += ' d_' + str(obj_dist)
        
        if laststatus != curstatus:
            status.setstatus(curstatus)
            laststatus = curstatus

if __name__ == '__main__':
    do_init()
    mainloop()
