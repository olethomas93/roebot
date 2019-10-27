
from communication import modbusTcp
from ImageProcessing import ImageProcessing
from ImageProcessing import test4
from threading import Thread, Lock




def main():


    tcpClient = modbusTcp.modbusClient()
    imageProcess = test4.imageProcessing()
    imageProcess.processImage()


    # test = tcpClient.getValue(2)
    #
    # if test:
    #     x,y = test2.processImage();
    #
    #     print(x,y)

















if __name__ == "__main__":
    main()




