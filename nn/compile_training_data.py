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
    td = nn.training_data()
    starttimer = time.time()
    numimages = td.process_samples(os.path.join(thisfilepath, 'sample_data/*'))

    endtimer = time.time()
    secs = endtimer - starttimer
    print(f"Processed {numimages} images in {secs} seconds.")

    # save training 'pickle'
    print('Saving file...')
    outfile = os.path.join(thisfilepath, 'training_data', 'rover.pkl')
    td.save_pickle(outfile)

    print('done.')

    exit()
