#!/usr/bin/python3
import os, time
import warnings
import rovercom
import hbridge
import servo

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
obj_dist = -1
try:
    import gpiozero
    distance_sensor = gpiozero.DistanceSensor(echo=17, trigger=4, max_distance=4, partial=True)
    for x in range(1, 5):
        time.sleep(1)
        if int(distance_sensor.distance) > 0:
            print('Distance sensor activated.')
            hasDistanceSensor = True
            break
except:
    hasDistanceSensor = False
    print('No distance sensor found.  Disabling ultrasonic features...')

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
    lcmd = cmd.lower()
    args = cmd.split()
    largs = lcmd.split()
    
    # logic for processing commands (add new ones here):
    if lcmd == 'quit':
        exit()

    if lcmd == 'poweroff':
        os.system('poweroff')

    if lcmd == 'stop':
        print('stop')
        # stop resets steering and sets throttle to zero:
        steering = 1
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
                steering = 0
            elif largs[1] == 'right':
                print('move right')
                throttle = 75
                steering = 1
            elif largs[1] == 'backwards':
                print('move backwards')
                throttle = -75
                steering = 0
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

def processcommand(cmds):
    if cmds == None:
         return

    if isinstance(cmds, str):
        cmds = []
        cmds.append(str)
        
    for cmd in cmds:
        processacommand(cmd)

def do_init():
    rovercom.init_fifos()
    print('Rover Daemon')
    hbridge.motor_off()
    hbridge.set_throttle(0)
    print('Init complete.')

def mainloop():
    global hasDistanceSensor, obj_dist, throttle, steering
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
            curstatus = '^   '
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
