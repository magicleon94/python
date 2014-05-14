import numpy as np
import cv2
drawing = False
mode = True
color = (0,0,255)
filled = -1
ix, iy = -1,-1
#mask = np.zeros((2,2),np.uint8)
def draw_shapes(event,x,y,flags,param):
    global drawing,mode,ix,iy,mask
    if event==cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x,y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                #cv2.rectangle(img,(0,0),(511,511),(0,0,0),-1)
                #cv2.floodFill(img,mask,(x,y),(0,0,0))
                cv2.rectangle(img,(ix,iy),(x,y),color,filled)
            else:
                #cv2.rectangle(img,(0,0),(511,511),(0,0,0),-1)
                #cv2.floodFill(img,mask,(x,y),(0,0,0))
                cv2.circle(img,(x,y),5,color,filled)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.rectangle(img,(ix,iy),(x,y),color,filled)
        else:
            cv2.circle(img,(x,y),5,color,filled)

img = np.zeros((512,512,3),np.uint8)
cv2.namedWindow('paint')
cv2.setMouseCallback('paint',draw_shapes)

while 1:
    cv2.imshow('paint',img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == ord('d'):
        color = (0,0,0)
    elif k == ord('c'):
        color = (0,0,255)
    elif k == ord('f'):
        if filled == -1:
            filled = 1
        else:
            filled = -1
    elif k == ord('q'):
        break
cv2.destroyAllWindows()
    
