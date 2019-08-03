#! /usr/bin/python2

from __future__ import division
from __future__ import print_function
import cv2


class GateCheck:

    def predict(self, ct, img=None):
        x, y, w, h = cv2.boundingRect(ct)
        ct_area = cv2.contourArea(ct)
        objAreaRatio = ct_area/float(w*h)
        ratioCond1 = ((h*2 > 0.75*w) and (h < 1.25*w))
        ratioCond2 = ((h*2 > 0.75*w) and (h*2 < 1.25*w))
        heightCond = True
        sizeCond = True
        if img is not None:
            heightCond = y/img.shape[0] < 0.7
            sizeCond = (float(w*h)/img.shape[0]/img.shape[1]) > 0.025 and (
                float(w*h)/img.shape[0]/img.shape[1]) < 0.90
        cropped = self.cropSix(img, ct)
        condLeg = self.condLeg(cropped)
        sumCond = objAreaRatio < 0.3 and (
            ratioCond1 or ratioCond2) and condLeg and sizeCond and heightCond
        if sumCond:
            return 1
        return 0

    def cropSix(self, img, ct):
        cropped = []
        x, y, w, h = cv2.boundingRect(ct)
        y = int((y+h)-(w*2)+h/3)
        if (y+h)-(w*2) < 0:
            y = int(y+h/5)
        for i in range(6):
            cropped.append(img[int(y+h/6):int(y+h*3/6),
                               int(x+i*w/6):int(x+(i+1)*w/6)])
            if cropped[i].shape[0] > 20 and cropped[i].shape[1] > 5:
                cv2.imshow(str(i), cropped[i])
        cv2.waitKey(1)
        return cropped

    def condLeg(self, cropped):
        for c in cropped:
            if c.size < 100:
                return False
        cond = True

        first = cropped[0].copy()
        first = first/255
        # print('first', first.sum()/first.size, end='\t')
        second = cropped[1].copy()
        second = second/255
        # print('second', second.sum()/second.size, end=' \t')
        cond = cond and (first.sum()/first.size > second.sum()/second.size)

        third = cropped[2].copy()
        third = third/255
        specialCond = (third.sum()/third.size > 0.05)
        # print('third', third.sum()/third.size, end='\t')
        fourth = cropped[3].copy()
        fourth = fourth/255
        specialCond = specialCond or (fourth.sum()/fourth.size > 0.05)
        cond = cond and specialCond
        # print('fourth', fourth.sum()/fourth.size, end=' \t')

        fifth = cropped[4].copy()
        fifth = fifth/255
        # print('fifth', fifth.sum()/fifth.size, end='\t')
        sixth = cropped[5].copy()
        sixth = sixth/255
        # print('sixth', sixth.sum()/sixth.size)
        cond = cond and (sixth.sum()/sixth.size > fifth.sum()/fifth.size)
        return cond
