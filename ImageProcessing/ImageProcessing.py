import threading
import cv2
import numpy as np


class imageProcessing:

    def __init__(self):

        self.processingQueue = []



     # def trackFilteredObjects(self,threshold,camerafeed):







    def update(self,image):

        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1920)

        # while (True):

    def detect(self,image):

             #Take each frame
             #_, frame = capture.read()



            #h = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            #w = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            #kSize = np.ones((35, 35), np.uint8)
            #grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #brightGray = cv2.convertScaleAbs(grayImage, -1, alpha=5, beta=10)
            ret, bwImage = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            StructureElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (35, 35))
            erodedImage = cv2.erode(bwImage, StructureElement)
            tresh = cv2.dilate(erodedImage, StructureElement)
            countors, _ = cv2.findContours(tresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            # Get the moments
            mu = [None] * len(countors)
            for i in range(len(countors)):
                mu[i] = cv2.moments(countors[i])

            # Get the mass centers, X & Y coordinates of blob
            mc = [None] * len(countors)
            for i in range(len(countors)):
                # add 1e-5 to avoid division by zero
                area = mu[i]['m00']
                if area > (1 * 1):
                    xCoor = mu[i]['m10'] / area + 1e-5
                    Ycoor = mu[i]['m01'] / area + 1e-5
                    heigth, width = tresh.shape

                    xCoor = width - xCoor
                    Ycoor = heigth - Ycoor
                    print(xCoor, Ycoor)

                    mc[i] = (mu[i]['m10'] / (mu[i]['m00'] + 1e-5), mu[i]['m01'] / (mu[i]['m00'] + 1e-5))


            # Draw contours

            drawing = np.zeros((tresh.shape[0], tresh.shape[1], 3), dtype=np.uint8)

            # draw circls around mass center of detected object
            for i in range(len(countors)):
                color = 255, 0, 0
                cv2.drawContours(drawing, countors, i, color, 2)
                cv2.circle(drawing, (int(mc[i][0]), int(mc[i][1])), 4, color, -1)
                cv2.drawContours(tresh, countors, -1, (0, 0, 255), 1)

            # cv2.imshow('gray', grayImage)
            # cv2.imshow('frame', frame)
            # cv2.imshow('bright', bwImage)
            #
            # # cv2.imshow('bw',img)
            # cv2.imshow('ele', drawing)
            #
            # k = cv2.waitKey(5) & 0xFF
            # if k == 27:
            #     break
        # capture.release()
        # cv2.destroyAllWindows()

    def elementsInProcessingQueue(self):
        if len(self.processingQueue) == 0:
            return 2
        else:
            return len(self.processingQueue)

    def runTilStackEmpty(self):

        while (True):

            if self.elementsInProcessingQueue() > 0:

                self.processImage()
            else:
                print("kroefoe")

    def run(self):

        t1 = threading.Thread(target=self.runTilStackEmpty)
        t1.start()


img = imageProcessing()
img.run()
