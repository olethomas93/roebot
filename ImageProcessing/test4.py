import cv2
import numpy as np
import random as rng
from picamera.array import PiRGBArray
from picamera import PiCamera
import imutils




class imageProcessing(object):

    def __init__(self):

        processingQueue = list



    def processImage(self):

        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 30
        rawCapture = PiRGBArray(camera, size=(640, 480))

        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

            image = frame.array
            imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(imgray, 200, 255, cv2.THRESH_BINARY)
            cimg = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

            c = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 0.5, 41, param1=70,
                                 param2=30, minRadius=3, maxRadius=30)
            c = np.uint16(np.around(c))

            for i in c[0, :]:
                # draw the outer circle
                cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # draw the center of the circle
                cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

            cv2.namedWindow('img', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('img', 800, 800)
            cv2.imshow('img', cimg)


            k = cv2.waitKey(5) & 0xFF

            if k == 27:
                break
            rawCapture.truncate(0)

        cv2.destroyAllWindows()
