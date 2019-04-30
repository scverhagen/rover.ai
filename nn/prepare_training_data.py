#!/usr/bin/python3
import cv2
import glob
import os
import numpy as np
import pandas as pd

labels = glob.glob('./sample_data/*')
for label in labels:
    

exit()



files = glob.glob('./center/*.jpg')
count = 0
for thisfile in files:
    image = cv2.imread(thisfile)
    image2 = image[240:480, 0:640]
    image2 = cv2.GaussianBlur(image2, (3, 3), 0)
    hsv = cv2.cvtColor(image2,cv2.COLOR_BGR2HSV)
    green_min = (70, 70, 100)
    green_max = (95, 150, 250)

    mask1 = cv2.inRange(hsv, green_min, green_max)
    target = cv2.bitwise_and(image2,image2, mask=mask1)

    cv2.imshow('clip', target)
    cv2.imshow('clip2', image)

    cv2.imwrite('c' + str(count) + '.jpg', target)

#    cv2.waitKey(0)
    count += 1
    #if count == 25:
    #    quit()