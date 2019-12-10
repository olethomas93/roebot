
from ImageProcessing import RoeImage
from datetime import datetime

class Camera:
    frame = None
    camToOpen = 0
    FOV = 90
    found = False
    timestamp = None


    def create(self, image, cameraHeigth, pictureIndex):

        result = RoeImage.RoeImage(cameraHeigth, self.FOV)

        now = datetime.now()
        timestamp = datetime.timestamp(now)
        self.frame = image


        self.timeStamp = timestamp

        result.setImage(self.frame)
        result.setTimeStamp(self.timeStamp)
        result.setPictureIndex(pictureIndex)


        return result
