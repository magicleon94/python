# -*- coding: utf-8 -*-
import numpy as np
import cv2

img = np.zeros((500,500,3), np.uint8)

cv2.ellipse(img,(250,100),(100,100),0,125,415,(0,0,255),-1)
cv2.circle(img,(250,100),45,(0,0,0),-1)

cv2.ellipse(img,(140,300),(100,100),0,0,297,(0,255,0),-1)
cv2.circle(img,(140,300),45,(0,0,0),-1)

cv2.ellipse(img,(375,300),(100,100),0,300,600,(255,0,0),-1)
cv2.circle(img,(375,300),45,(0,0,0),-1)


cv2.imshow('boh',img)
while 1:
    print cv2.waitKey(0) & 0xFF

#non preciso nelle angolazioni ma il concetto c'è
