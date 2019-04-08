'''
This is first script to detect gate in ROBOSub 2018.
'''

import math
import cv2


class Gate:
    ''' GATE Processing class. You can use this class to process ROBOSUB gate mission.
    Parameters:
        fileOrDevice (str,int): you can send this to OpenCV to open
    '''

    def __init__(self, fileToOpen):
        self.device = cv2.VideoCapture(fileToOpen)

    def read(self):
        '''Read openned file and openImg Window
        '''

        while self.device.isOpened():
            retval, image = self.device.read()
            if not retval:
                break
            small_image = cv2.resize(image, None, fx=0.5, fy=0.5)
            processed = self._process(small_image)
            cv2.imshow('raw', small_image)
            # cv2.imshow('blur', processed[3])
            # cv2.imshow('h', processed[0])
            # cv2.imshow('s', processed[1])
            cv2.imshow('v', processed[2])
            cv2.imshow('v_edges', processed[4])
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

    def _process(self, img):
        img_size = img.shape[0:2]
        k_size = int(img_size[0]/60)
        k_size += (k_size % 2)-1
        blured = cv2.medianBlur(img, k_size)
        hsv = cv2.cvtColor(blured, cv2.COLOR_BGR2HSV)
        _h, _s, _v = cv2.split(hsv)
        (_mu, sigma) = cv2.meanStdDev(_v)
        edges = cv2.Canny(img, _mu - sigma, _mu + sigma)
        lines = cv2.HoughLinesP(
            edges, 1, math.pi/180, 70, minLineLength=img_size[0]/15, maxLineGap=img_size[0]/80)
        if lines is not None:
            for line in lines:
                _l = line[0]
                p_1 = _l[0:2]
                p_2 = _l[2:4]
                angle = math.atan2(p_1[1] - p_2[1], p_1[0] - p_2[0])
                if abs(angle-math.pi/2) < math.pi*30/180:
                    # print(angle)
                    cv2.line(img, (_l[0], _l[1]), (_l[2], _l[3]),
                             (0, 0, 255), 3, cv2.LINE_AA)
        return (_h, _s, _v, blured, edges, lines)
