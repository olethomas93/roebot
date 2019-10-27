import cv2
import numpy as np
import random as rng
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread, Lock

regs_lock = Lock()


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
            kSize = np.ones((35, 35), np.uint8)
            kernel = np.ones((5, 5), np.float32) / 25
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            grayImage = cv2.filter2D(grayImage, -1, kernel)
            grayImage = cv2.convertScaleAbs(grayImage, -1, alpha=1, beta=10)
            ret, bwImage = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            StructureElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            erodedImage = cv2.erode(bwImage, StructureElement)
            dilatedImage = cv2.dilate(erodedImage, StructureElement)


            countors, _ = cv2.findContours(dilatedImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            # Get the moments
            mu = [None] * len(countors)
            for i in range(len(countors)):
                mu[i] = cv2.moments(countors[i])

            # Get the mass centers, X & Y coordinates of blob
            mc = [None] * len(countors)
            for i in range(len(countors)):
                # add 1e-5 to avoid division by zero

                xCoor = mu[i]['m10'] / (mu[i]['m00'] + 1e-5)
                Ycoor = mu[i]['m01'] / (mu[i]['m00'] + 1e-5)
                heigth, width = dilatedImage.shape

                xCoor = width - xCoor
                Ycoor = heigth - Ycoor

                # cor = Coordinate.Coordinate(xCoor, Ycoor)

                # print(cor.xCoord)

                mc[i] = (mu[i]['m10'] / (mu[i]['m00'] + 1e-5), mu[i]['m01'] / (mu[i]['m00'] + 1e-5))

            # Draw contours

            drawing = np.zeros((dilatedImage.shape[0], dilatedImage.shape[1], 3), dtype=np.uint8)

            # draw circls around mass center of detected object
            for i in range(len(countors)):
                color = 255, 0, 0
                cv2.drawContours(drawing, countors, i, color, 2)
                cv2.circle(drawing, (int(mc[i][0]), int(mc[i][1])), 4, color, -1)
                cv2.drawContours(image, countors, -1, (0, 0, 255), 1)

            cv2.imshow('gray', grayImage)
            cv2.imshow('bwimage',dilatedImage)
            cv2.imshow('frame', image)
            cv2.imshow('bright', drawing)
            #cv2.imshow('keypoints', with_key_points)

            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
            rawCapture.truncate(0)

        cv2.destroyAllWindows()
