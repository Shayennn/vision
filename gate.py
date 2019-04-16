'''
This is first script to detect gate in ROBOSub 2018.
'''

import math
import numpy as np
import cv2


class Gate:
    ''' GATE Processing class. You can use this class to process ROBOSUB gate mission.
    Parameters:
        fileOrDevice (str,int): you can send this to OpenCV to open
    '''

    def __init__(self, fileToOpen):
        self.device = cv2.VideoCapture(fileToOpen)
        self.filename = fileToOpen
        self.history = []
        self.history_limit = 5
        self.last_detect = None

    def read(self):
        '''Read openned file and openImg Window
        '''

        while self.device.isOpened():
            retval, image = self.device.read()
            if not retval:
                break
            small_image = cv2.resize(image, None, fx=0.25, fy=0.25)
            processed = self._process(small_image)
            cv2.imshow(self.filename+' ct', processed[4])
            if processed[5] is not None:
                diff = self.calcDiffPercent(processed[5], self.last_detect)
                cond = self.last_detect is None or diff[0] < 0.4
                if cond:
                    self.last_detect = processed[5]
            if self.last_detect is not None:
                print(self.last_detect)
            key = cv2.waitKey(10)
            if key == ord('q'):
                break

    def _process(self, img):
        def my_area(ct):
            x, y, w, h = cv2.boundingRect(ct)
            return w*h
        img_size = img.shape[0:2]
        k_size = int(img_size[0]/80)
        k_size += (k_size % 2)-1
        blured = cv2.medianBlur(img, k_size)
        gray = cv2.cvtColor(blured, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(
            int(img_size[0]*0.15), int(img_size[0]*0.15)))
        gray = clahe.apply(gray)

        (_mu, sigma) = cv2.meanStdDev(gray)
        edges = cv2.Canny(img, _mu - 1.25*sigma, _mu + 1.25*sigma)

        slide_box_size = int(img_size[0]*0.02)
        noise_thresh = edges.sum()/edges.size
        if _mu > 127:
            for i in range(len(edges)-slide_box_size):
                interest_area = edges[i:i+slide_box_size]
                if interest_area.sum()/interest_area.size > noise_thresh*0.8:
                    interest_area.fill(0)

        cts, hi = cv2.findContours(edges, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
        cts = sorted(cts, key=my_area, reverse=True)
        found = None
        withct = img.copy()
        for c in cts:
            x, y, w, h = cv2.boundingRect(c)
            if (cv2.contourArea(c)/w/h > 0.4) or w*h/edges.size < 0.02:
                continue
            else:
                # withct = cv2.drawContours(withct, [c], 0, (0, 255, 255), 3)
                found = ((2*x+w)/img.shape[1]-1, (2*y+h)/img.shape[0] -
                         1, 2*x/img.shape[1]-1, 2*(x+w)/img.shape[1]-1)
                diff = self.calcDiffPercent(found, self.last_detect)
                cond = self.last_detect is None or diff[0] < 0.3
                if cond:
                    cv2.rectangle(withct, (x, y), (x+w, y+h), (255, 255, 0), 3)
                    cv2.circle(withct, (int(x+w/2), int(y+h/2)),
                               4, (0, 255, 255), 4)
                    break
        return (gray, blured, edges, cts, withct, found)

    def calcDiffPercent(self, first, second):
        if first is None or second is None or len(first) < len(second):
            return [0]
        res = []
        for key, val in enumerate(first):
            res.append(abs(val-second[key])*2/(val+second[key]+2))
        return tuple(res)
