import cv2
import numpy as np
import random as rng
from picamera.array import PiRGBArray
from picamera import PiCamera







class imageProcessing(object):

    def __init__(self):

        processingQueue = list



    def processImage(self):
        def nothing(x):
            pass

        cv2.namedWindow('temp')
        cv2.createTrackbar('bl', 'temp', 0, 255, nothing)
        cv2.createTrackbar('gl', 'temp', 0, 255, nothing)
        cv2.createTrackbar('rl', 'temp', 0, 255, nothing)
        cv2.createTrackbar('bh', 'temp', 255, 255, nothing)
        cv2.createTrackbar('gh', 'temp', 255, 255, nothing)
        cv2.createTrackbar('rh', 'temp', 255, 255, nothing)


        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 30
        rawCapture = PiRGBArray(camera, size=(640, 480))

        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

            image_color = frame.array
            image_ori = cv2.cvtColor(image_color,cv2.COLOR_BGR2GRAY)

            bl_temp = cv2.getTrackbarPos('bl', 'temp')
            gl_temp = cv2.getTrackbarPos('gl', 'temp')
            rl_temp = cv2.getTrackbarPos('rl', 'temp')

            bh_temp = cv2.getTrackbarPos('bh', 'temp')
            gh_temp = cv2.getTrackbarPos('gh', 'temp')
            rh_temp = cv2.getTrackbarPos('rh', 'temp')


            lower_bound = np.array([0, 0, 10])
            upper_bound = np.array([255, 255, 195])

            image = image_color
            mask = cv2.inRange(image, (bl_temp, gl_temp, rl_temp), (bh_temp, gh_temp, rh_temp))

           # mask = cv2.inRange(image, lower_bound, upper_bound)
            thresh = cv2.inRange(image, (0, 0, 255), (255, 255, 255))

            # mask = cv2.adaptiveThreshold(image_ori,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            #             cv2.THRESH_BINARY_INV,33,2)

            kernel = np.zeros((3, 3), np.uint8)

            # Use erosion and dilation combination to eliminate false positives.
            # In this case the text Q0X could be identified as circles but it is not.
            # thresh = cv2.erode(thresh, kernel, iterations=6)
            # thresh = cv2.dilate(thresh, kernel, iterations=3)

            closing = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

            contours,_ = cv2.findContours(thresh.copy(), cv2.RETR_LIST,
                                        cv2.CHAIN_APPROX_SIMPLE)
            #contours.sort(key=lambda x: cv2.boundingRect(x)[0])

            array = []
            ii = 1

            len(contours)
            for c in contours:
                (x, y), r = cv2.minEnclosingCircle(c)
                center = (int(x), int(y))
                r = int(r)
                if r >= 5 and r <= 20:
                    print(center)



                    cv2.circle(image, center, r, (0, 255, 0), 2)
                    array.append(center)

            cv2.imshow("preprocessed", image_color)
            cv2.imshow('tresh',thresh)
            cv2.imshow('prosessed',image)
            cv2.imshow('masked',mask)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
            rawCapture.truncate(0)

        cv2.destroyAllWindows()



