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
        camera.resolution = (1920, 1080)
        camera.framerate = 30
        rawCapture = PiRGBArray(camera, size=(1920, 1080))

        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

            image = frame.array
            kSize = np.ones((35, 35), np.uint8)

            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            grayImage = cv2.convertScaleAbs(grayImage, -1, alpha=2, beta=10)
            ret, bwImage = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            StructureElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (35, 35))
            erodedImage = cv2.erode(bwImage, StructureElement)
            dilatedImage = cv2.dilate(erodedImage, StructureElement)
            params = cv2.SimpleBlobDetector_Params()
            params.filterByCircularity = True
            params.minCircularity = 0.1
            detector = cv2.SimpleBlobDetector()
            keypoints = detector.detect(dilatedImage)

            with_key_points = cv2.drawKeypoints(image, keypoints, np.array([]), (0, 0, 255),
                                                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            # draw circls around mass center of detected object


            cv2.imshow('keypoints', with_key_points)

            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
            rawCapture.truncate(0)

        cv2.destroyAllWindows()