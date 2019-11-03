
class RoeImage:
    roePositionPixels = []
    roePositionMillimeters = []
    FOV = None
    timeStamp = None
    Image = None
    captureHeight = 0

    def __init__(self, captureHeight, fieldOfView):
        self.captureHeight = captureHeight
        self.FOV = fieldOfView

    def setImage(self, image):
        self.image = image

    def getImage(self):
        return self.image

    def setTimeStamp(self, timeStamp):
        self.timeStamp = timeStamp

    def getTimeStamp(self):
        return self.timeStamp

    def addRoePositionPixel(self, coordinate):

        self.roePositionPixels.append(coordinate)

    def getRoePositionPixel(self):
        return self.roePositionPixels

    def addRoePositionMillimeter(self, coordinate):
        self.roePositionMillimeters.append(coordinate)


    def getRoePositionMillimeter(self):
        return self.roePositionMillimeters

    # Set picture index in coordinate system
    # @param pictureIndex of picture

    def setPictureIndex(self, pictureIndex):
        self.pictureIndex = pictureIndex

    def getPictureIndex(self):
        return self.pictureIndex

    def getFieldOfView(self):
        return self.FOV

    def getDistance(self):
        return self.captureHeight
