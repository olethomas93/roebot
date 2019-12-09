import cv2
import numpy as np

from threading import Thread, Lock
import cmath as math
from ImageProcessing.Coordinate import coordinate

regs_lock = Lock()


class imageProcessing(object):

    def __init__(self, debug=True):

        self.processingQueue = []

        self.debug = debug

    def processImages(self):
        imageList = []

        for roeImage in self.processingQueue:

            print("processing images" + str(roeImage.getPictureIndex()))

            image = roeImage.getImage()

            #tresholds image for detection of Roe
            thresh = cv2.inRange(image, (210, 0, 0), (255, 255, 255))


            # mask = cv2.adaptiveThreshold(image_ori,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            #             cv2.THRESH_BINARY_INV,33,2)

            kernel = np.zeros((3, 3), np.uint8)

            # Use erosion and dilation combination to eliminate false positives.
            # In this case the text Q0X could be identified as circles but it is not.
            # thresh = cv2.erode(thresh, kernel, iterations=6)
            # thresh = cv2.dilate(thresh, kernel, iterations=3)
            #detecting circles in tresholded image with a specific radius
            detected_circles = cv2.HoughCircles(thresh.copy(),
                                                cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                                                param2=6, minRadius=3, maxRadius=40)

            if detected_circles is not None:

                # Convert the circle parameters a, b and r to integers.
                detected_circles = np.uint16(np.around(detected_circles))

                for pt in detected_circles[0, :]:
                    x, y, r = pt[0], pt[1], pt[2]


                    cord = coordinate(x, y)
                    cv2.circle(image, (x,y), r, (0, 255, 0), 2)
                    self.pixelToMillimeterConversion(cord, roeImage)

            # add image to imagelist

            imageList.append(roeImage)
            if self.debug:

                cv2.imwrite('prosessed'+str(roeImage.getPictureIndex())+".png", image)
                cv2.imwrite('tresh.png',thresh)

        if len(imageList) >= 2:
            self.processingQueue = []

            return imageList, True
        else:
            None, False


    #converts pixel-coordinates to milimeter coordinates

    def pixelToMillimeterConversion(self, coord, roe):
        fieldOfView = roe.getFieldOfView()
        distance = roe.getDistance()
        height, width, _ = roe.getImage().shape
        imageHeigth = height
        imageWidth = width

        # calculate length of diagonal of image in mm
        diagonalMillimeter = float(distance) * math.tan((fieldOfView / 2) * (math.pi / 180)) * 2

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

        xPositionMillimeter = coord.getxCoor() * pixelSizeDirX

        yPositionMillimeter = coord.getyCoor() * pixelSizeDirY

        millimeterCoordinate = coordinate(int(round(xPositionMillimeter.real, 2)),
                                          int(round(yPositionMillimeter.real, 2)))
        roe.addRoePositionMillimeter(millimeterCoordinate)
