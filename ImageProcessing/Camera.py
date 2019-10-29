import cv2
from ImageProcessing import RoeImage
import time
from picamera.array import PiRGBArray
from picamera import PiCamera



class Camera:
    frame = None
    camToOpen = 0
    FOV = 62
    found = False
    timestamp = None






    def takePicture(self, cameraHeigth, pictureIndex):
        camera = PiCamera()
        camera.resolution=(640,480)
        rawCapture = PiRGBArray(camera, size=(640, 480))


        result = RoeImage.RoeImage(cameraHeigth, self.FOV)
        self.frame = camera.capture(rawCapture, format="bgr")


        self.timeStamp = int(round(time.time() * 1000))

        result.setImage(self.frame)
        result.setTimeStamp(self.timeStamp)
        result.setPictureIndex(pictureIndex)

        return result