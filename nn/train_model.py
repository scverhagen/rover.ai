#!/usr/bin/python3
import cv2
import glob
import os
import time
import numpy as np
import pandas as pd
import pickle
import nn

thisfilepath = os.path.dirname(__file__)

if __name__ == '__main__':
    starttimer = time.time()

    # load training data pickle:
    print('Loading training data set...')
    picklefilename = os.path.join(thisfilepath, 'training_data', 'rover.pkl')
    td = nn.training_data()
    td.load_pickle(picklefilename)
    
    print('Initializing neural network...')
    thisnet = nn.dnn_tf()
    print('Training...')
    
    thisnet.train(td)
    
    endtimer = time.time()
    secs = round(endtimer - starttimer, 2)
    print(f"Neural network training completed in {secs} seconds.")
    print('Testing model accuracy...')
    y = thisnet.predict(td.X_test)
    #print(y.argmax(-1))
    #print(y)
    #print(td.y_test.argmax(-1))
    
    #y_true = y.argmax(-1)
    accuracy = np.mean(y.argmax(-1) == td.y_test.argmax(-1))
    print('Model accuracy is: ' + str(accuracy))

    print('Saving model...')
    nnfilename = os.path.join(thisfilepath, 'nn_model')
    #thisnet.save(nnfilename)
    

    exit()
