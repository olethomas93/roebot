import cv2
import numpy as np
import random as rng
from picamera.array import PiRGBArray
from picamera import PiCamera
import imutils




class imageProcessing(object):

    def __init__(self):

        processingQueue = list

    def is_contour_bad(c):
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # the contour is 'bad' if it is not a rectangle
        return not len(approx) == 4

    def processImage(self):

        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 30
        rawCapture = PiRGBArray(camera, size=(640, 480))

        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

            image = frame.array
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edged = cv2.Canny(gray, 50, 100)
            cv2.imshow("Original", image)

            cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            mask = np.ones(image.shape[:2], dtype="uint8") * 255

            # remove the contours from the image and show the resulting images
            image = cv2.bitwise_and(image, image, mask=mask)
            cv2.imshow("Mask", mask)
            cv2.imshow("After", image)
            k = cv2.waitKey(5) & 0xFF

            if k == 27:
                break
            rawCapture.truncate(0)

        cv2.destroyAllWindows()
