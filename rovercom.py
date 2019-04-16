import os

thisfilepath = os.path.dirname(__file__)
fifopath = thisfilepath + '/rover_cmd'
fifobuffersize = 100


def init_fifo():
    try:
        os.mkfifo(fifopath)
    except:
        pass

def checkforcommand():
    try:
        file = os.open(fifopath, os.O_RDONLY | os.O_NONBLOCK)
        incmd = os.read(file, fifobuffersize)
        os.close(file)
        incmd = incmd.decode('utf-8')
    except:
        incmd = ''
    
    return incmd.strip()

def sendcommand(cmd):
    try:
        with open(fifopath, 'w') as fifo:
            fifo.write(cmd)
    except:
        pass
    
