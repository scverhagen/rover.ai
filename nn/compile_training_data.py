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

def main():

    starttimer = time.time()
    count = 0
    
    # define dictionary and arrays:
    datadict = {'X':[], 'y':[]}
    X = [] # data
    y = [] # label
    labeldict = {'label':[], 'name':[]}
    labelkeys = []
    labelnames = []

    labels = glob.glob(os.path.join(thisfilepath, 'sample_data/*'))
    for label in labels:
        if os.path.isdir(label) == True:
            thislabel = os.path.basename(label)
            thislabelname = thislabel
            if os.path.isfile(label + '.name'):
                with open(label + '.name', 'r') as file:
                    thislabelname = file.readline().strip()

            # add label names to lists:
            labelkeys.append(thislabel)
            labelnames.append(thislabelname)

            print(f"Processing data for label: {thislabelname}...")

            pics = glob.glob(os.path.join(label, '*'))
            for pic in pics:
                img = cv2.imread(pic)
                img2 = nn.convertframefornn(img).flatten()

                X.append(img2)
                y.append(thislabel)
                count += 1

    # add arrays to dictionary and convert to pandas dataframe:
    datadict['X'] = X
    datadict['y'] = y
    df = pd.DataFrame(datadict)

    # add arrays to label dictionary and converto to pandas dataframe:
    labeldict['label'] = labelkeys
    labeldict['name'] = labelnames
    ldf = pd.DataFrame(labeldict)

    endtimer = time.time()
    secs = endtimer - starttimer
    print(f"Processed {count} images in {secs} seconds.")

    # save training 'pickle'
    print('Saving file...')

    training_data = {'labels': ldf, 'data': df}
    outfile = os.path.join(thisfilepath, 'training_data', 'rover.pkl')
    with open(outfile, 'wb') as filehandle:
        pickle.dump(training_data, filehandle, pickle.HIGHEST_PROTOCOL)

    print('done.')

    exit()

if __name__ == '__main__':
    main()