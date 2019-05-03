import cv2
import glob
import os
import pickle
import numpy as np
import pandas as pd

def convertframefornn(img):
    # crop the image:
    image2 = img[240:480, 0:640]
    
    # blur the image:
    #image2 = cv2.GaussianBlur(image2, (3, 3), 0)

    # convert the image to grayscale:
    image2bw = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # convert the image to hsv and create mask for green tape:
    hsv = cv2.cvtColor(image2,cv2.COLOR_BGR2HSV)
    green_min = (60, 70, 100)
    green_max = (95, 150, 250)
    mask = cv2.inRange(hsv, green_min, green_max)

    # apply mask to grayscale image
    target = cv2.bitwise_and(image2bw,image2bw, mask=mask)
    return target.flatten()

def label_to_onehot(count, labelnum):
    onehot = []
    for i in range(0, count):
        if i == labelnum:
            onehot.append(1)
        else:
            onehot.append(0)
    return onehot

class ann:
    def __init__(self):
        self.thisnet = cv2.ml.ANN_MLP_create()
        self.thisnet.setLayerSizes(np.int32([(640*240), 48, 4]))
        self.thisnet.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)
        self.thisnet.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM, 2, 0)

    def train(self, training_data):
        #print(training_data.data['X'])
        #print(training_data.data['y'])
        self.thisnet.train(np.float32(training_data.data['X']), cv2.ml.ROW_SAMPLE, np.float32(training_data.data['y']))
        
    def predict(self, X):
        ret, resp = self.thisnet.predict(np.float32(X))
        return resp.argmax(-1)

    def load(self, filename):
        self.thisnet = cv2.ml.ANN_MLP_load(filename)

    def save(self, filename):
        self.thisnet.save(filename)

class training_data(object):
    def __init__(self):
        labeldict = {}
        data = {}

    def load_pickle(self, filename):
        #clear/reset class vars:
        self.labeldict = {}
        self.data = pd.DataFrame()

        with open(filename, "rb") as filehandle:
            training_data = pickle.load(filehandle)
        #print(training_data)
        self.labeldict = training_data['labels']
        self.data = training_data['data']

    def save_pickle(self, filename):
        training_data = {'labels': self.labeldict, 'data': self.data}
        with open(filename, 'wb') as filehandle:
            pickle.dump(training_data, filehandle, pickle.HIGHEST_PROTOCOL)
            
    def process_samples(self, sampledir):
        #clear/reset class vars:
        self.labeldict = {}
        self.data = pd.DataFrame()

        # define temp dictionary and arrays:
        datadict = {}
        X = [] # data
        y = [] # label

        labels = glob.glob(sampledir)
        
        # get label count
        labelcount = 0
        for label in labels:
            if os.path.isdir(label) == True:
                labelcount += 1
        
        samplecount = 0

        for label in labels:
            if os.path.isdir(label) == True:
                thislabel = os.path.basename(label)
                thislabelname = thislabel
                if os.path.isfile(label + '.name'):
                    with open(label + '.name', 'r') as file:
                        thislabelname = file.readline().strip()

                # add label name and key to dictionary
                self.labeldict[thislabel] = thislabelname

                print(f"Processing data for label: {thislabelname}...")

                pics = glob.glob(os.path.join(label, '*.jpg'))
                for pic in pics:
                    img = cv2.imread(pic)
                    img2 = convertframefornn(img)

                    X.append(img2)
                    #y.append(label_to_onehot(labelcount, int(thislabel)))
                    y.append(int(thislabel))
                    samplecount += 1

        # add arrays to dictionary (with rescaled X data):
        datadict['X'] = (np.array(X) / 255) 
        datadict['y'] = np.array(y)

        # Populate training_data class and write to file:

        self.data = datadict
        return samplecount
    