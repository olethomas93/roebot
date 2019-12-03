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

    def takePicture(self, cameraHeigth, pictureIndex):
        # camera = PiCamera()
        # camera.resolution=(640,480)
        # rawCapture = PiRGBArray(camera, size=(640, 480))
        result = RoeImage.RoeImage(cameraHeigth, self.FOV)
        with picamera.PiCamera() as camera:

            with picamera.array.PiRGBArray(camera) as output:
                camera.resolution = (1920, 1080)
                camera.start_preview()
                sleep(2)
                camera.capture(output, format='bgr')

                self.frame = output.array

        self.timeStamp = "imagestamp"

        result.setImage(self.frame)
        result.setTimeStamp(self.timeStamp)
        result.setPictureIndex(pictureIndex)
        print(result.getTimeStamp())

        return result
