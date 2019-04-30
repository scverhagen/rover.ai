import cv2

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
    return target

class ann:
    def __init__(self):
        self.thisnet = cv2.ml.ANN_MLP_create()
        self.thisnet.setLayerSizes( (640*240), 16, 4)
        self.thisnet.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)
        self.thisnet.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM, cv2.ml.TrainFlags.NO_INPUT_SCALE, cv2.ml.TrainingMethods.BACKPROP)

