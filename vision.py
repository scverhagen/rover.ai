#!/usr/bin/python3
import os
import pandas as pd
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import nn.nn

thisfilepath = os.path.dirname(__file__)

print('Loading neural network...')
thisnet = nn.nn.dnn_tf()
thisnet.load()

def decision_from_frame(img):
    # 0 forward
    # 1 left
    # 2 right

    img2 = nn.nn.convertframefornn(img, flatten=True)

    X = np.float32(img2)
    X = np.array([X])
    #print(str(img2.shape))

    y = thisnet.predict(X)[0]
    return y.argmax(-1)

def training_test():
    print('Loading training data...')
    td = nn.nn.training_data()
    td.load_pickle(os.path.join(thisfilepath, 'nn', 'training_data', 'rover.pkl'))

    y = thisnet.predict(td.X_test).argmax(-1)
    y_test = td.y_test.argmax(-1)

    acc = accuracy = (np.mean(y == y_test) * 100)
    print('y vs y_test:')
    print('Accuracy: ' + str(round(acc, 1)) + '%')

if __name__ == '__main__':
    print('Testing computer vision:')

    img = cv2.imread(os.path.join(thisfilepath, 'nn', 'sample_data', '0', 'i_219.jpg'))
    dec = decision_from_frame(img)
    print(dec)
    
    cap = cv2.VideoCapture(0)
    ret = cap.set(3,640)
    ret = cap.set(4,480)

    while(True):
        ret, frame = cap.read()
        print(decision_from_frame(frame))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
