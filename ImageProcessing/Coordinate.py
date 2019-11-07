class coordinate(object):

    def __init__(self, xCoord=-1, yCoord=-1, zCoord=-1):
        self.xCoord = xCoord
        self.YCoord = yCoord
        self.zCoord = zCoord

    def getxCoor(self):
        return self.xCoord

    def getyCoor(self):
        return self.YCoord

    def getzCoor(self):
        return self.zCoord

    def getCoord(self):
        return self.xCoord, self.YCoord
