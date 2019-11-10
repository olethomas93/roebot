from pyModbusTCP.client import ModbusClient
from communication import r_w_float_modbus
from communication import modbusTcp
import time
from threading import Thread, Lock
from ImageProcessing import Coordinate
from ImageProcessing import Camera
from ImageProcessing import imageProcessing2
import random

SERVER_HOST = "192.168.137.65"
SERVER_PORT = 2000

# init a thread lock
regs_lock = Lock()
regList = []

class roebot():

    def __init__(self, threadpool):
        self.tp = Thread(target=self.polling_thread)
        self.threadpool = threadpool
        self.tp.start()
        self.pictureIndex = 0
        self.camera = Camera.Camera()
        self.imageCv = imageProcessing2.imageProcessing()
        self.imageList = []

        # self.modbusclient = r_w_float_modbus.FloatModbusClient(ModbusClient)

    def poll_command(self, ):
        print("Polling server for commands")

        # display loop (in main thread)
        while True:
            # print regs list (with thread lock synchronization)
            with regs_lock:
                if regList:
                    command = regList[0]
                    print(command)
                    if command in range(1, 4):
                        self.sendIntModbus(0,0)
                        self.switch_case(command)
            # 1s before next print
            time.sleep(1)

    def waitForCommands(self, waitCommand):
        print("started")
        wait = True
        while wait:
            command, wait = self.getCommand()
            if command == waitCommand:
                self.modbusclient.sendInt(0, 0)
                return True, command

    def getValueFromRegister(self, indexNmbr):
        wait = False
        while not wait:
            with regs_lock:
                if self.regList:
                    value = self.regList[indexNmbr]
                    if value > 0:
                        wait = True
                        return value

    # Takes picture of tray.
    def takePicture(self):
        print("Executing take picture")

        RoeImage = self.camera.takePicture(330, self.pictureIndexindex)
        self.pictureIndex += 1
        self.imageCv.processingQueue.append(RoeImage)
        self.switch_case(0)

    # modbus polling thread
    def polling_thread(self):
        global regList
        self.client = ModbusClient(host=SERVER_HOST, port=SERVER_PORT)
        isOpen = False
        # polling loop
        while True:
            # keep TCP open
            if not self.client.is_open():
                print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))
                self.client.open()

            if self.client.is_open():
                if not isOpen:
                    print("connected to " + SERVER_HOST + ":" + str(SERVER_PORT))
                    isOpen = True

            # do modbus reading on socket
            reg_list = self.client.read_holding_registers(0, 10)
            print(reg_list)
            # if read is ok, store result in regs (with thread lock synchronization)
            if reg_list:
                with regs_lock:
                    regList = list(reg_list)
            # 1s before next polling
            time.sleep(1)

    # send int to modbusServer
    def sendIntModbus(self, value, address):

        result = self.client.write_single_register(address, value)
        return result

    # process images by creating a RoeImage adding them to roeimage Queue
    def processImages(self):

        if len(self.imageList) == 0:
            print("processing images")
            imageList, processing = self.imageCv.processImages()
            self.imageList = imageList
        else:
            self.imageList = []
            self.processImages()

        self.switch_case(0)

    def sendcoord(self, arrayX, arrayY):
        print(arrayY)
        for i in range(0, len(arrayY)):
            self.sendIntModbus(int(arrayY[i]), i + 10)

        for i in range(0, len(arrayX)):
            self.sendIntModbus(int(arrayX[i]), i + 50)

    # generate coordinate list relative to the robot

    def generatecoordinateList(self):
        coordList = []
        for roeImage in self.imageList:
            if len(roeImage.getRoePositionMillimeter())>0:

                for i in range(len(roeImage.getRoePositionMillimeter())):

                    coordinate = roeImage.getRoePositionMillimeter()[i]

                    xpos = coordinate.getxCoor() + i* 300
                    ypos = coordinate.getyCoor()

                    newcoord = Coordinate.coordinate(xpos,ypos)

                    coordList.append(newcoord)



        return coordList

    def sendCordToPLC(self):
        arrayX = []
        arrayY = []
        corrdList = self.generatecoordinateList()
        for cord in corrdList:
            arrayX.append(cord.getxCoor())
            arrayY.append(cord.getyCoor())

        self.sendcoord(arrayX, arrayY)
        self.switch_case(0)

    def switch_case(self, command):

        switcher = {
            0: self.poll_command,
            2: self.takePicture,
            3: self.processImages,
            4: self.sendCordToPLC
        }
        # Get the function from switcher dictionary
        func = switcher.get(command, lambda: "Invalid command")
        # Execute the function
        return func()
