import cv2
import numpy as np
import random as rng
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread, Lock
from ImageProcessing import Coordinate
import cmath as math

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
            thresh = cv2.inRange(image.copy(), (0, 0, 0), (213, 255, 255))
            kSize = np.ones((35, 35), np.uint8)
            kernel = np.ones((5, 5), np.float32) / 25
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            grayImage = cv2.GaussianBlur(thresh, (5, 5), 0)
            grayImage = cv2.convertScaleAbs(grayImage, -1, alpha=-2, beta=10)
            edged = cv2.Canny(thresh, 10, 40)  # 10 and 40 to be more perceptive
            ret, bwImage = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            StructureElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            erodedImage = cv2.erode(thresh, StructureElement)
            dilatedImage = cv2.dilate(erodedImage, StructureElement)

            countors, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

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

                cor = Coordinate.Coordinate(xCoor, Ycoor)
                self.pixelToMillimeterConversion(cor,)

                # print(cor.xCoord)

                mc[i] = (mu[i]['m10'] / (mu[i]['m00'] + 1e-5), mu[i]['m01'] / (mu[i]['m00'] + 1e-5))

            # Draw contours

            drawing = np.zeros((dilatedImage.shape[0], dilatedImage.shape[1], 3), dtype=np.uint8)

            # draw circls around mass center of detected object
            for i in range(len(countors)):
                color = 255, 0, 0
                approx = cv2.approxPolyDP(countors, 0.01 * cv2.arcLength(countors, True), True)
                cv2.drawContours(drawing, countors, i, color, 2)
                cv2.circle(drawing, (int(mc[i][0]), int(mc[i][1])), 4, color, -1)
                cv2.drawContours(image, countors, -1, (0, 0, 255), 1)

            cv2.imshow('image', image)
            cv2.imshow('bwimage', dilatedImage)
            cv2.imshow('frame', thresh)
            cv2.imshow('bright', drawing)
            # cv2.imshow('keypoints', with_key_points)

            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
            rawCapture.truncate(0)

        cv2.destroyAllWindows()

    def pixelToMillimeterConversion(self, coordinate, RoeImage):
        fieldOfView = RoeImage.getFieldOfView()
        distance = RoeImage.getDistance()
        imageHeigth = RoeImage.getImage().heigth()
        imageWidth = RoeImage.getImage().width()

        # calculate length of diagonal of image in mm
        diagonalMillimeter = distance * math.tan((fieldOfView / 2) * (math.pi / 180)) * 2

        # calculate angle of diagonal
        theta = math.atan(imageHeigth / imageWidth)

        # calculate width of image in milimeter
        imageWidthMillimeter = math.cos(theta) * diagonalMillimeter

        # calculate heigth of image in millimeter
        imageHeigthInMillimeter = math.sin(theta) * diagonalMillimeter

        # calculate the size of a pixel in x directon in mm
        pixelSizeDirX = imageHeigthInMillimeter / imageHeigth

        # calculate the size of a pixel in y directon in mm
        pixelSizeDirY = imageWidthMillimeter / imageWidth

        xPositionMillimeter = coordinate.getxCoord() * pixelSizeDirY

        yPositionMillimeter = coordinate.getyCoord() * pixelSizeDirX

        millimeterCoordinate = Coordinate.Coordinate(xPositionMillimeter, yPositionMillimeter)
        RoeImage.addRoePositionMillimeter(millimeterCoordinate)