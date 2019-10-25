from ImageProcessing import ImageProcessing
from communication import modbusTcp




def main():
    tcpClient = modbusTcp.modbusClient()
    image = ImageProcessing.imageProcessing()
    image.processImage()
    tcpClient.polling_thread()


if __name__ == "__main__":
    main()




