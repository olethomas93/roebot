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
    FOV = 62
    found = False
    timestamp = None






    def takePicture(self, cameraHeigth, pictureIndex):
        # camera = PiCamera()
        # camera.resolution=(640,480)
        #rawCapture = PiRGBArray(camera, size=(640, 480))

        with picamera.PiCamera() as camera:
            with picamera.array.PiRGBArray(camera) as output:
                camera.capture(output, 'rgb')
                print('Captured %dx%d image' % (
                    output.array.shape[1], output.array.shape[0]))

        result = RoeImage.RoeImage(cameraHeigth, self.FOV)

        self.frame = camera.capture('rawCapture.jpg')


        self.timeStamp = int(round(time.time() * 1000))

        result.setImage(self.frame)
        result.setTimeStamp(self.timeStamp)
        result.setPictureIndex(pictureIndex)

        return result