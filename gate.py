'''
This is first script to detect gate in ROBOSub 2018.
'''

import cv2


class gate:
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
            smallImage = cv2.resize(image, None, fx=0.5, fy=0.5)
            cv2.imshow('raw', smallImage)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
