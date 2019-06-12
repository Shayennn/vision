#! /usr/bin/python2

from keras.models import load_model
import numpy as np
import cv2


class GateML:

    def __init__(self):
        self.model = load_model('gate_model.h5')
        
    def predict(self, img):
        return self.predict_multi([img])[0]

    def predict_multi(self, imgs):
        x = []
        for img in imgs:
            histed = cv2.equalizeHist(img)
            x.append(histed)
        x = np.array(x)
        x = x.reshape(x.shape[0], 20, 40, 1)
        return self.model.predict_classes(x)

    def getprop(self, imgs):
        x = []
        for img in imgs:
            histed = cv2.equalizeHist(img)
            x.append(histed)
        x = np.array(x)
        x = x.reshape(x.shape[0], 20, 40, 1)
        return self.model.predict(x)
