'''
This is first script to detect gate in ROBOSub 2018.
'''

import cv2

device = cv2.VideoCapture('test.mp4')

while device.isOpened():
    retval, image = device.read()
    if not retval:
        break
    smallImage = cv2.resize(image, None, fx=0.5, fy=0.5)
    cv2.imshow('raw', smallImage)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
