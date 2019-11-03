from concurrent.futures import ThreadPoolExecutor
import threading
from pyModbusTCP.client import ModbusClient
from communication import r_w_float_modbus
from ImageProcessing import Camera
from ImageProcessing import imageProcessing2
import random


Roeimages = []

def waitForCommands():
    print("started")
    wait = True
    modbusclient = r_w_float_modbus.FloatModbusClient(host='158.38.140.52',port=2000,auto_open=True)

    while wait:
        command, wait = modbusclient.read_float(0)
        command = int(command[0])
        print(str(command)+" ----"+"command")
        if command == 0:
            wait = True
        if command >0:
            modbusclient.close()
            modbusclient.write_float(0,[0])
            switch_case(command)

def takePicture():
    print("Executing take picture")
    camera = Camera.Camera()
    RoeImage = camera.takePicture(80,1)
    Roeimages.append(RoeImage)




    switch_case(1)


def processImages():
    imageCv = imageProcessing2.imageProcessing()
    for image in Roeimages:

        imageCv.processImage(image)

def switch_case(command):
    switcher = {
        1: waitForCommands,
        2: takePicture,
        3: processImages
    }
    # Get the function from switcher dictionary
    func = switcher.get(command, lambda: "Invalid command")
    # Execute the function
    return func()


def main():
    executor = ThreadPoolExecutor(max_workers=3)
    task1 = executor.submit(switch_case(1))
    task2 = executor.submit(switch_case(3))


if __name__ == '__main__':
    main()
