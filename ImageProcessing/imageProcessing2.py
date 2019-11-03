import cv2
import numpy as np
import random as rng
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread, Lock
import cmath as math
from ImageProcessing.Coordinate import coordinate
regs_lock = Lock()


class imageProcessing(object):

    def __init__(self,debug):

        self.corArray = []
        processingQueue = list
        self.debug = debug

    def processImage(self, roeImage):

        image_color = roeImage.getImage()

        image_ori = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)

        lower_bound = np.array([0, 0, 10])
        upper_bound = np.array([255, 255, 195])

        image = image_color

        mask = cv2.inRange(image, lower_bound, upper_bound)
        thresh = cv2.inRange(image_color, (255, 0, 0), (255, 255, 255))
        # gh = 230
        cv2.imwrite('tresh.png',thresh)
        # mask = cv2.adaptiveThreshold(image_ori,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
        #             cv2.THRESH_BINARY_INV,33,2)

        kernel = np.zeros((3, 3), np.uint8)

        # Use erosion and dilation combination to eliminate false positives.
        # In this case the text Q0X could be identified as circles but it is not.
        # thresh = cv2.erode(thresh, kernel, iterations=6)
        # thresh = cv2.dilate(thresh, kernel, iterations=3)

        closing = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        _,contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_LIST,
                                       cv2.CHAIN_APPROX_SIMPLE)
        # contours.sort(key=lambda x: cv2.boundingRect(x)[0])

        array = []
        ii = 1
        ii = 1

        len(contours)
        for c in contours:
            (x, y), r = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            r = int(r)
            if r >= 0.8 and r <= 5:
                print(center)
                cord = coordinate(center[0], center[1])
                self.corArray.append(cord)
                cv2.circle(image, center, r, (0, 255, 0), 2)
                array.append(center)
                self.pixelToMillimeterConversion(cord,roeImage)

        if self.debug:



            cv2.imwrite('prosessed %d.png', image)


    def pixelToMillimeterConversion(self, coord, RoeImage):
        fieldOfView = RoeImage.getFieldOfView()
        distance = RoeImage.getDistance()
        width, height,_ = RoeImage.getImage().shape
        imageHeigth = height
        imageWidth = width

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

        xPositionMillimeter = coord.getxCoor() * pixelSizeDirY

        yPositionMillimeter = coord.getyCoor() * pixelSizeDirX

        millimeterCoordinate = coordinate(xPositionMillimeter, yPositionMillimeter)
        RoeImage.addRoePositionMillimeter(millimeterCoordinate)
