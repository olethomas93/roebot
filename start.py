
from communication import modbusTcp
from ImageProcessing import ImageProcessing
from threading import Thread, Lock




def main():


    tcpClient = modbusTcp.modbusClient()
    imageProcess = ImageProcessing.imageProcessing()


    test = tcpClient.getValue(2)

    if test:
        x,y = imageProcess.processImage();

        print(x,y)

















if __name__ == "__main__":
    main()




