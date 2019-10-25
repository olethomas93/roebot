from ImageProcessing import ImageProcessing
from communication import modbusTcp




def main():

    image = ImageProcessing.imageProcessing()
    image.processImage()
    tcpClient = modbusTcp.modbusClient()
    tcpClient.polling_thread()


if __name__ == "__main__":
    main()




