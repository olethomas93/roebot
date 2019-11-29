import cv2
from ImageProcessing import RoeImage
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import picamera


class Camera:
    frame = None
    camToOpen = 0
    FOV = 78
    found = False
    timestamp = None

    def takePicture(self, image,cameraHeigth, pictureIndex):
        # camera = PiCamera()
        # camera.resolution=(640,480)
        # rawCapture = PiRGBArray(camera, size=(640, 480))
        result = RoeImage.RoeImage(cameraHeigth, self.FOV)


        self.frame = image

        self.timeStamp = "imagestamp"

        result.setImage(self.frame)
        result.setTimeStamp(self.timeStamp)
        result.setPictureIndex(pictureIndex)
        print(result.getTimeStamp())

        return result
