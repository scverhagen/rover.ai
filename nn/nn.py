import cv2
import glob
import os
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
import pickle
import numpy as np
import pandas as pd

thisfilepath = os.path.dirname(__file__)

def convertframefornn(img=None, flatten=True):
    #resize image:
    img = cv2.resize(img,(320,240))
    
    # crop the image:
    #image2 = img[240:480, 0:640]
    image2 = img[120:240, 0:320]
    
    # blur the image:
    #image2 = cv2.GaussianBlur(image2, (5, 5), 0)

    # convert the image to grayscale:
    image2bw = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # convert the image to hsv and create mask for green tape:
    hsv = cv2.cvtColor(image2,cv2.COLOR_BGR2HSV)
    green_min = (60, 70, 100)
    green_max = (95, 150, 250)
    mask = cv2.inRange(hsv, green_min, green_max)
    

    # apply mask to grayscale image
    target = cv2.bitwise_and(image2bw,image2bw, mask=mask)
    if flatten == True:
        return target.flatten()
    else:
        return target

def label_to_onehot(count, labelnum):
    onehot = []
    for i in range(0, count):
        if i == labelnum:
            onehot.append(1)
        else:
            onehot.append(0)
    return onehot

class dnn_tf:
    def __init__(self):
        pass

    def train(self, td):
        numentries, px = td.X_train.shape
        numentries, outlayersize = td.y_train.shape
        
        #self.thisnet = keras.Sequential([keras.layers.Flatten(input_shape=(153600, )), keras.layers.Dense(196, activation=tf.nn.sigmoid), keras.layers.Dense(outlayersize, activation=tf.nn.sigmoid)])
        self.thisnet = keras.Sequential([keras.layers.Flatten(input_shape=(38400, )), keras.layers.Dense(196, activation=tf.nn.sigmoid), keras.layers.Dense(outlayersize, activation=tf.nn.sigmoid)])
        # 88.8% self.thisnet.compile(optimizer=tf.train.AdamOptimizer(learning_rate=0.015), loss=keras.losses.sparse_categorical_crossentropy, metrics=['accuracy'])
        # 81% self.thisnet.compile(optimizer=tf.train.AdagradOptimizer(learning_rate=0.005), loss=keras.losses.sparse_categorical_crossentropy, metrics=['accuracy'])

        # 92.6%:
        self.thisnet.compile(optimizer=tf.train.RMSPropOptimizer(learning_rate=0.03), loss=keras.losses.sparse_categorical_crossentropy, metrics=['accuracy'])
        self.thisnet.fit(np.float32(td.X_train), np.float32(td.y_train.argmax(-1)), epochs=25)
        
    def predict(self, X):
        y = self.thisnet.predict(X)
        return y

    def load(self, filename=''):
        filename = os.path.join(thisfilepath, 'tf_model')

        self.thisnet = tf.keras.models.load_model(filename)
        self.thisnet.compile(optimizer=tf.train.RMSPropOptimizer(learning_rate=0.03), loss=keras.losses.sparse_categorical_crossentropy, metrics=['accuracy'])

    def save(self, filename=''):
        if filename == '':
            filename = os.path.join(thisfilepath, 'tf_model')
        #saved_model_path = tf.contrib.saved_model.save_keras_model(self.thisnet, filename)
        tf.keras.models.save_model(self.thisnet, filename)

class ann:
    def __init__(self):
        self.thisnet = cv2.ml.ANN_MLP_create()

    def train(self, td):
        numentries, px = td.X_train.shape
        numentries, outlayersize = td.y_train.shape
        
        #print(td.X_train)
        self.thisnet.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)
        self.thisnet.setLayerSizes(np.int32([px, 32, outlayersize]))
        self.thisnet.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM, 0, 0)
        self.thisnet.train(np.float32(td.X_train), cv2.ml.ROW_SAMPLE, np.float32(td.y_train))
        
    def predict(self, X):
        ret, resp = self.thisnet.predict(np.float32(X))
        return resp

    def load(self, filename=''):
        if filename == '':
            filename = os.path.join(thisfilepath, 'nn_model')
        self.thisnet = cv2.ml.ANN_MLP_load(filename)

    def save(self, filename=''):
        self.thisnet.save(filename)

class training_data(object):
    def __init__(self):
        self.data = pd.DataFrame()
       
    def load_pickle(self, filename):
        self.data = pd.DataFrame()

        with open(filename, "rb") as filehandle:
            self.data = pickle.load(filehandle)
        
        self.update_train_test_split()
            
    def update_train_test_split(self):
        X = self.data['frame'].as_matrix()
#        print(X)
        y = self.data.as_matrix(columns=self.data.columns[1:])
#        print(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        self.X_train = np.float32(list(X_train))
        self.X_test = np.float32(list(X_test))
        self.y_train = np.float32(list(y_train))
        self.y_test = np.float32(list(y_test))

    def save_pickle(self, filename):
        with open(filename, 'wb') as filehandle:
            pickle.dump(self.data, filehandle, pickle.HIGHEST_PROTOCOL)
            
    def process_samples(self, sampledir):
        self.data = pd.DataFrame()
        samplecount = 0

        labels = glob.glob(sampledir)
        labels.sort()
        
        pdcolumnnames = []
        pdcolumnnames.append('frame')
        
        # get labels
        for label in labels:
            if os.path.isdir(label) == True:
                thislabel = os.path.basename(label)
                thislabelname = thislabel
                if os.path.isdir(label) == True:
                    if os.path.isfile(label + '.name'):
                        with open(label + '.name', 'r') as file:
                            thislabelname = file.readline().strip()
                pdcolumnnames.append(thislabelname)

        rows = []
        for label in labels:
            if os.path.isdir(label) == True:
                thislabel = os.path.basename(label)
                thislabelname = thislabel
                if os.path.isfile(label + '.name'):
                    with open(label + '.name', 'r') as file:
                        thislabelname = file.readline().strip()

                print('Processing data for label: ' + thislabelname + '...')
                pics = glob.glob(os.path.join(label, '*.jpg'))
                for pic in pics:
                    img = cv2.imread(pic)
                    img2 = convertframefornn(img)

                    thisrow = {'frame': img2, thislabelname: 1}
                    rows.append(thisrow)
                    samplecount += 1

        self.data = pd.DataFrame(columns=pdcolumnnames, data=rows)
        self.data.fillna(0, inplace=True)

        self.update_train_test_split()

        return samplecount
    
