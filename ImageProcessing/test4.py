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
        cv2.createTrackbar('rl', 'temp', 0, 100, nothing)
        cv2.createTrackbar('ru', 'temp', 100, 100, nothing)


        camera = PiCamera()
        camera.resolution = (1640, 922)
        camera.framerate = 24
        rawCapture = PiRGBArray(camera, size=(1640, 922))

        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

            image_color = frame.array
            image_ori = cv2.cvtColor(image_color,cv2.COLOR_BGR2GRAY)
            image_ori = cv2.GaussianBlur(image_ori, (5, 5), 0)
            bl_temp = cv2.getTrackbarPos('bl', 'temp')
            gl_temp = cv2.getTrackbarPos('gl', 'temp')
            rl_temp = cv2.getTrackbarPos('rl', 'temp')

            bh_temp = cv2.getTrackbarPos('bh', 'temp')
            gh_temp = cv2.getTrackbarPos('gh', 'temp')
            rh_temp = cv2.getTrackbarPos('rh', 'temp')
            radiusl = cv2.getTrackbarPos('rl', 'temp')
            radiusu = cv2.getTrackbarPos('ru', 'temp')



            lower_bound = np.array([0, 0, 10])
            upper_bound = np.array([255, 255, 195])

            image = image_color
            mask = cv2.inRange(image, (bl_temp, gl_temp, rl_temp), (bh_temp, gh_temp, rh_temp))

           # mask = cv2.inRange(image, lower_bound, upper_bound)
            thresh = cv2.inRange(image_color, (255, 0, 0), (255, 255, 255))

            #gh = 230

            # mask = cv2.adaptiveThreshold(image_ori,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            #             cv2.THRESH_BINARY_INV,33,2)

            kernel = np.zeros((3, 3), np.uint8)

            # Use erosion and dilation combination to eliminate false positives.
            # In this case the text Q0X could be identified as circles but it is not.
            # thresh = cv2.erode(thresh, kernel, iterations=6)
            # thresh = cv2.dilate(thresh, kernel, iterations=3)



            closing = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            detected_circles = cv2.HoughCircles(mask.copy(),
                                                cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                                                param2=10, minRadius=1, maxRadius=40)
            _,contours,_ = cv2.findContours(mask.copy(), cv2.RETR_LIST,
                                        cv2.CHAIN_APPROX_SIMPLE)
            #contours.sort(key=lambda x: cv2.boundingRect(x)[0])

            array = []
            ii = 1
            if detected_circles is not None:
                print("fefe")
                # Convert the circle parameters a, b and r to integers.
                detected_circles = np.uint16(np.around(detected_circles))

                for pt in detected_circles[0, :]:
                    a, b, r = pt[0], pt[1], pt[2]

                    # Draw the circumference of the circle.
                    cv2.circle(image, (a, b), r, (0, 255, 0), 2)

                    cv2.circle(image, (a, b), 1, (0, 0, 255), 3)




            cv2.imshow("processed", image)
            cv2.imshow('masked',mask)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
            rawCapture.truncate(0)

        cv2.destroyAllWindows()



