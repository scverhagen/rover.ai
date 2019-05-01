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
    thisnet = nn.ann()
    print('Training...')
    thisnet.train(td)
    
    print('Saving model...')
    nnfilename = os.path.join(thisfilepath, 'nn_model')
    thisnet.save(nnfilename)
    
    endtimer = time.time()
    secs = round(endtimer - starttimer, 2)
    print(f"Neural network training completed in {secs} seconds.")
    print('done.')

    exit()
