#!/usr/bin/python3
import os
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
    td.load_pickle(os.path.join(thisfilepath, 'nn' , 'training_data', 'rover.pkl'))
    
    X_train, X_test, y_train, y_test = train_test_split(td.data['X'], td.data['y'], test_size=0.33, random_state=42)
    
    td.data['X'] = X_train
    td.data['y'] = y_train
    
    print('Training neural network...')
    thisnet.train(td)
    
    y_pred = thisnet.predict(X_test)
    print(y_pred)
    print(y_test[0])
    print(confusion_matrix(y_test, y_pred))
