
from communication import modbusTcp
from ImageProcessing import ImageProcessing
from ImageProcessing import test3
from threading import Thread, Lock




def main():


    tcpClient = modbusTcp.modbusClient()
    #imageProcess = ImageProcessing.imageProcessing()
    test2 = test3.imageProcessing()
    test2.processImage()

    # test = tcpClient.getValue(2)
    #
    # if test:
    #     x,y = test2.processImage();
    #
    #     print(x,y)

















if __name__ == "__main__":
    main()




