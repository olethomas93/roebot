import numpy as np
import imutils
import cv2


class roeDetector:
    def __init__(self, accumWeight=0.5):
        # store the accumulated weight factor
        self.accumWeight = accumWeight

        # initialize the background model
        self.bg = None

    def update(self, image):
        # if the background model is None, initialize it
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return

        # update the background model by accumulating the weighted
        # average
        cv2.accumulateWeighted(image, self.bg, self.accumWeight)

    def detect(self, image, tVal=25):

      # threshold the image

        # thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]
        mask = cv2.inRange(image, (210, 0, 0), (255, 255, 255))

        grayImage = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

        StructureElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        erodedImage = cv2.erode(mask, StructureElement)
        dilatedImage = cv2.dilate(erodedImage, StructureElement)

        detected_circles = cv2.HoughCircles(dilatedImage.copy(),
                                            cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                                            param2=7, minRadius=3, maxRadius=10)

        cv2.imwrite('masked', mask.copy())

        cv2.imwrite('gray.jpg', grayImage.copy())

        cv2.imwrite('eroded.jpg', erodedImage.copy())

        cv2.imwrite('dilated.jpg', dilatedImage.copy())

        # perform a series of erosions and dilations to remove small
        # blobs
        # thresh = cv2.erode(thresh, None, iterations=2)
        # thresh = cv2.dilate(thresh, None, iterations=2)
        # find contours in the thresholded image and initialize the
        # minimum and maximum bounding box regions for motion
        # cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        # cv2.CHAIN_APPROX_SIMPLE)

        # cnts = imutils.grab_contours(cnts)
        # (minX, minY) = (np.inf, np.inf)
        # (maxX, maxY) = (-np.inf, -np.inf)
        # if no contours were found, return None

        if detected_circles is not None:

            if len(detected_circles) == 0:
                return None


            detected_circles = np.uint16(np.around(detected_circles))



        return mask, detected_circles
