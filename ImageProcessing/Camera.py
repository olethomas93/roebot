import cv2
import ImageProcessing.RoeImage
import time


class Camera:

    def __init__(self):
        self.found = False
        self.camToOpen = 0
        self.FOV = 78

    def Camera(self):
        self.cap = cv2.VideoCapture(self.camToOpen)
        if not self.cap.isOpened():
            raise Exception("Could not open video device")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    def takePicture(self, cameraHeigth, pictureIndex):
        result = RoeImage.RoeImage(cameraHeigth, self.FOV)

        _, self.frame = self.cap.read()

        self.timeStamp = int(round(time.time() * 1000))

        result.setImage(self.frame)
        result.setTimeStamp(self.timeStamp)
        result.setPictureIndex(pictureIndex)

        return result