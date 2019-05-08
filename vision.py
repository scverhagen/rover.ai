#!/usr/bin/python3
import os
import pandas as pd
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import settings
import nn.nn

thisfilepath = os.path.dirname(__file__)

print('Loading settings...')
roversettings = settings.settings()

print('Initializing video capture...')
global cap
cap = cv2.VideoCapture(roversettings.dict['videosource'])
ret = cap.set(3,640)
ret = cap.set(4,480)

print('Loading neural network...')
thisnet = nn.nn.dnn_tf()
thisnet.load()

def test():
    pass

class vdq_class(object):
    
    def __init__(self, queue_length = 3):
        self.decision_queue = []
        self.queue_length = queue_length

    def add(self, dec):
        self.decision_queue.append(int(dec))
        
        if len(self.decision_queue) > self.queue_length:
            self.decision_queue.pop(0)

    def mean(self):
        return round(sum(self.decision_queue) / len(self.decision_queue))

    def process_img(self, img):
        self.add(decision_from_frame(img))
        
vdq = vdq_class()

def decision_from_frame(img):
    global vdq
    # 0 forward
    # 1 left
    # 2 right

    img2 = nn.nn.convertframefornn(img, flatten=True)

    X = np.float32(img2)
    X = np.array([X])
    #print(str(img2.shape))

    # get value from neural network:
    y = thisnet.predict(X)[0]

    # convert value form onehot to int and add to vision decision queue (vdq):
    vdq.add(int(y.argmax(-1)))
    
    # return value of vdq:
    return vdq.mean()

def training_test():
    print('Loading training data...')
    td = nn.nn.training_data()
    td.load_pickle(os.path.join(thisfilepath, 'nn', 'training_data', 'rover.pkl'))

    y = thisnet.predict(td.X_test).argmax(-1)
    y_test = td.y_test.argmax(-1)

    acc = accuracy = (np.mean(y == y_test) * 100)
    print('y vs y_test:')
    print('Accuracy: ' + str(round(acc, 1)) + '%')

def get_video_frame():
    ret, frame = cap.read()
    return frame

def get_next_decision():
    frame = get_video_frame()
    return decision_from_frame(frame)

if __name__ == '__main__':
    
    print('Testing computer vision:')

    ret = cap.set(3,640)
    ret = cap.set(4,480)

    while(True):
        ret, frame = cap.read()
        
        print(decision_from_frame(frame))
        #print(frame)
        cv2.imshow('frame', frame)
        cv2.imshow('filtered', nn.nn.convertframefornn(frame, flatten=False))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
