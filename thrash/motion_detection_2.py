import numpy as np
import cv2
import imutils

cap = cv2.VideoCapture('456.mp4')  # Open video file
#cap = cv2.VideoCapture('123.mp4')  # Open video file
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)  # Create the background substractor
kernelOp = np.ones((3, 3), np.uint8)
kernelCl = np.ones((11, 11), np.uint8)
areaTH = 500

while (cap.isOpened()):
    ret, frame = cap.read()  # read a frame
    frame = imutils.resize(frame, width=700)
    fgmask = fgbg.apply(frame)  # Use the substractor

    try:
        ret, imBin = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
        # Opening (erode->dilate) para quitar ruido.
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
        # Closing (dilate -> erode) para juntar regiones blancas.
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernelCl)
    except:
        # if there are no more frames to show...
        print('EOF')
        break

    line2 = np.array([[450, 0], [450, 200]], np.int32).reshape((-1, 1, 2))
    frame = cv2.polylines(frame, [line2], False, (0, 0, 255), thickness=1)


    _, contours0, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours0:
        #cv2.drawContours(frame, cnt, -1, (0, 255, 0), 3, 8)
        area = cv2.contourArea(cnt)
        if area > areaTH:
            #################
            #   TRACKING    #
            #################
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Frame', frame)

    # Abort and exit with 'Q' or ESC
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()  # release video file
cv2.destroyAllWindows()  # close all openCV windows
