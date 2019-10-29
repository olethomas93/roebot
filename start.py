
from communication import r_w_float_modbus

from ImageProcessing import imageProcessing2

from ImageProcessing import Camera



def main():



    tcpClient = r_w_float_modbus.FloatModbusClient(host='localhost', port=2000, auto_open=True)

    if True:
        command = tcpClient.read_float(0)
        switch(int(command))

        tcpClient.close()



def takePicture():
    camera = Camera.Camera()
    image = camera.takePicture(80, 1)
    processImage(image)


def processImage(image):
    imageProcess = imageProcessing2.imageProcessing()
    imageProcess.processImage(image)


def switch(i):
    switcher = {
        1: takePicture

    }
    func = switcher.get(i, lambda: 'Invalid')
    return func()


if __name__ == '__main__':

    main()
