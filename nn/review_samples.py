#!/usr/bin/python3
import cv2
import glob
import os
import time
import numpy as np
import pandas as pd
import json

import nn

thisfilepath = os.path.dirname(__file__)

def main():

    print('This script will allow you to review samples.')
    print('---------------------------------------------')
    print('If a sample is acceptable, press the space bar.')
    print('If you would like to delete a sample, press the d key.')
    print('At any time you can cancel by pressing the ESC key.')
    print('---------------------------------------------')
    print('Press enter key to continue...')
    blah = input()

    count = 0

    labels = glob.glob(os.path.join(thisfilepath, 'sample_data', '*'))
    for label in labels:
        thislabel = os.path.basename(label)
        print(f"Processing label: {thislabel}...")

        pics = glob.glob(os.path.join(label, '*'))
        for pic in pics:
            img = cv2.imread(pic)
            img2 = nn.convertframefornn(img, flatten=False)

            cv2.imshow(label, img)
            cv2.imshow('output', img2)

            keycode = cv2.waitKey(0)
            print(keycode)
            if keycode == 27:
                print('Escape key pressed.')
                cv2.destroyAllWindows()
                exit()

            if keycode == 100:
                os.remove(pic)
                print(f"{pic} deleted.")

            count += 1
#        cv2.destroyWindow(thislabel)

    cv2.destroyAllWindows()
    print('done.')

    exit()



if __name__ == '__main__':
    main()