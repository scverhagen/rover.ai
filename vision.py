#!/usr/bin/python3
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import nn.nn

thisfilepath = os.path.dirname(__file__)

thisnet = nn.nn.ann()
thisnet.load(os.path.join(thisfilepath, 'nn', 'nn_model'))

def decision_from_frame(img):
    # [1,0,0,0] stop
    # [0,1,0,0] forward
    # [0,0,1,0] left
    # [0,0,0,1] right

    img2 = nn.nn.convertframefornn(img)

if __name__ == '__main__':
    print('Loading training data...')
    td = nn.nn.training_data()
    td.load_pickle(os.path.join(thisfilepath, 'nn', 'training_data', 'rover.pkl'))

    #print('X_train Data')
    #print('Shape: ' + str(td.X_train.shape))
    #print('Type: ' + str(type(td.X_train)))
    #print(td.X_train)
    #print(' ')
    #print('y_train Data')
    #print('Shape: ' + str(td.y_train.shape))
    #print('Type: ' + str(type(td.y_train)))

    print('Training neural network...')
    thisnet.train(td)
    
    #y_pred = thisnet.predict(X_test)
    #print(y_pred)
    #print(y_test[0])
    #print(confusion_matrix(y_test, y_pred))
