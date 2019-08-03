from __future__ import division
from __future__ import print_function
import cv2
import numpy as np


class Gate:
    ''' GATE Processing class.
    You can use this class to process ROBOSUB gate mission.
    Parameters:
        fileOrDevice (str,int): you can send this to OpenCV to open
    '''

    def __init__(self, fileToOpen=None):
        if fileToOpen is not None:
            self.device = cv2.VideoCapture(fileToOpen)
        else:
            self.device = None
        self.filename = fileToOpen
        self.clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(13, 13))
        self.okrange = 67
        self.okval = 163

    def adjustVal(self, th):
        self.okval = th

    def adjustRange(self, th):
        self.okrange = th

    def read(self):
        '''Read opedgesenned file and openImg Window
        '''
        cv2.namedWindow(str(self.filename)+' ct')
        cv2.createTrackbar('val', str(self.filename)+' ct',
                           self.okval, 180, self.adjustVal)
        cv2.createTrackbar('TileGridSize', str(self.filename)+' ct',
                           self.okrange, 180, self.adjustRange)
        read = True
        while self.device.isOpened():
            if read:
                retval, image = self.device.read()
            if not retval:
                break
            self.doProcess(image, True)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            if key == ord('s'):
                read = not read

    def doProcess(self, img, showImg=False):
        """Put image then get outputs

        Arguments:
            img {OpenCV Image} -- Input image

        Keyword Arguments:
            showImg {bool} -- Wanna Show Img for debugging ? (default: {False})

        Returns:
            list -- Found data. None or list of cx1,cy1,cx2,cy2,area
        """
        img = cv2.resize(img, None, fx=0.50, fy=0.50)
        processed = self._process(img)
        if showImg:
            cv2.imshow(str(self.filename)+' raw', img)
            cv2.imshow(str(self.filename)+' ct', processed[1])
            cv2.imshow(str(self.filename)+' 2', processed[2])
        # if processed[6] is not None:
        #     diff = self.calcDiffPercent(processed[6], self.last_detect)
        #     cond = self.last_detect is None or diff[0] < 0.2
        #     if cond:
        #         self.last_detect = processed[6]
        return (processed[3], processed[1], processed[2])

    def _process(self, img):
        # img = cv2.resize(img, None, fx=0.5,fy=0.5)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        interest = cv2.extractChannel(hsv, 1)
        mask = cv2.inRange(interest, self.okval-self.okrange,
                           self.okval+self.okrange)
        kernel = np.ones((10, 3), np.uint8)
        noise_removed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        noise_removed = cv2.medianBlur(noise_removed, 9)
        _, cts, hi = cv2.findContours(noise_removed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        def getHigh(ct):
            x,y,w,h = cv2.boundingRect(ct)
            return h

        blank = np.zeros_like(interest, np.uint8)

        _found=0
        # _found = ((2*x+w)/img.shape[1]-1, (2*y+h)/img.shape[0]-1,
        #           2*x/img.shape[1]-1, 2*(x+w)/img.shape[1]-1,
        #           c_area/w/h, (2*w)/img.shape[1])
        return (img, mask, noise_removed, _found)

    def calcDiffPercent(self, first, second):
        if first is None or second is None or len(first) < len(second):
            return [0]
        res = []
        for key, val in enumerate(first):
            res.append(abs(val-second[key])/2)
        return tuple(res)
