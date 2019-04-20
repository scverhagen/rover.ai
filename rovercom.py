#!/usr/bin/python3

import os

thisfilepath = os.path.dirname(__file__)
cmdfifopath = thisfilepath + '/rover_cmd'
statusfifopath = thisfilepath + '/rover_status'
fifobuffersize = 100

def init_fifos():
    if not os.path.exists(cmdfifopath):
        os.mkfifo(cmdfifopath)
    else:
        os.remove(cmdfifopath)
        os.mkfifo(cmdfifopath)
    
def checkforcommand():
    try:
        file = os.open(cmdfifopath, os.O_RDONLY | os.O_NONBLOCK)
        incmd = os.read(file, fifobuffersize)
        os.close(file)
        incmd = incmd.decode('utf-8')
    except:
        incmd = ''
    
    return incmd.strip()

def sendcommand(cmd):
    try:
        with open(cmdfifopath, 'w') as fifo:
            fifo.write(cmd)
    except:
        pass
    
class status_fifo(object):
    def setstatus(self, statustxt):
        fifohandle = os.open(statusfifopath, os.O_TRUNC | os.O_WRONLY | os.O_CREAT)
        os.write(fifohandle, str.encode(statustxt + '\n'))
        os.close(fifohandle)

    def getstatus(self):
        #try:
        fifohandle = os.open(statusfifopath, os.O_RDONLY)
        data = os.read(fifohandle, 100)
        os.close(fifohandle)
        stata = data.decode()
        #except:
        #    stata = ''
        return stata
        
