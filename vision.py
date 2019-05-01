#!/usr/bin/python3
import os
import cv2

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
    #td = nn.nn.training_data()
    #print('loading training pickle...')
    #td.load_pickle(os.path.join(thisfilepath, 'nn', 'training_data', 'rover.pkl'))
    
    picfile = os.path.join(thisfilepath, 'nn', 'sample_data', '3', 'i3_412.jpg')

    img = cv2.imread(picfile)
    img2 = nn.nn.convertframefornn(img)
    
    print('making prediction...')

    X = []
    X.append(img2)
        
    print('predicted vals:')
    print(thisnet.predict(X))
    
