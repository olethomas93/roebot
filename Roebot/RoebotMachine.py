from pyModbusTCP.client import ModbusClient
import time
from threading import Thread, Lock
from ImageProcessing import Coordinate
from ImageProcessing import Camera
from ImageProcessing import imageProcessing2

SERVER_HOST = "192.168.137.65"
SERVER_PORT = 2000

# init a thread lock
regs_lock = Lock()


class roebot():

    def __init__(self, threadpool):
        self.tp = Thread(target=self.polling_thread)
        self.threadpool = threadpool
        self.regList = []
        self.tp.start()
        self.pictureIndex = 0
        self.camera = Camera.Camera()
        self.imageCv = imageProcessing2.imageProcessing()
        self.imageList = []

        # self.modbusclient = r_w_float_modbus.FloatModbusClient(ModbusClient)

    def poll_command(self):
        print("Polling server for commands")
        commandpoll = False
        # display loop (in main thread)
        while not commandpoll:

            # print regs list (with thread lock synchronization)

            if self.regList:
                command = self.regList[0]
                print(command)
                if command in range(1, 6):

                   if self.sendIntModbus(0, 0):

                        self.switch_case(command)



    # Takes picture of tray.
    def takePicture(self):
        print("Executing take picture")

        RoeImage = self.camera.takePicture(330, self.pictureIndex)
        self.pictureIndex += 1
        self.imageCv.processingQueue.append(RoeImage)
        self.switch_case(0)

    # modbus polling thread
    def polling_thread(self):
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
            # if read is ok, store result in regs (with thread lock synchronization)
            if reg_list:
                with regs_lock:
                    self.regList = list(reg_list)
            # 1s before next polling
            time.sleep(0.2)

    # send int to modbusServer
    def sendIntModbus(self, value, address):

        return self.client.write_single_register(address, value)


    # process images by creating a RoeImage adding them to roeimage Queue
    def processImages(self):

        if len(self.imageList) == 0:
            print("processing images")
            imageList1, processing = self.imageCv.processImages()
            self.imageList = imageList1
        else:
            self.imageList = []

        self.switch_case(0)

    def sendcoord(self, arrayX, arrayY):
        sending = False

        if self.client.write_multiple_registers(10, arrayX):
            print("write ok")
            sending = True
        else:
            print("write error")
            sending = False

        return sending
    # generate coordinate list relative to the robot

    def generatecoordinateList(self):
        print("generating cordinate list")
        coordList = []
        for roeImage in self.imageList:
            list = roeImage.getRoePositionMillimeter()
            if len(roeImage.getRoePositionMillimeter()) > 0:



                for i in range(len(list)):
                    coordinate = list[i]

                    xpos = coordinate.getxCoor() + (int(roeImage.getPictureIndex()) * 300)
                    ypos = coordinate.getyCoor()

                    newcoord = Coordinate.coordinate(xpos, ypos)

                    coordList.append(newcoord)

        return coordList

    def sendCordToPLC(self):
        arrayX = []
        arrayY = []
        corrdList = self.generatecoordinateList()
        for cord in corrdList:
            arrayX.append(cord.getxCoor())
            arrayY.append(cord.getyCoor())

        self.client.write_multiple_registers(10, arrayX)

        time.sleep(1)


        self.switch_case(0)

    def getImageList(self):
        print(len(self.imageList))

    def switch_case(self, command):

        switcher = {
            0: self.poll_command,
            2: self.takePicture,
            3: self.processImages,
            4: self.sendCordToPLC,
            5: self.getImageList

        }
        # Get the function from switcher dictionary
        func = switcher.get(command, lambda: "Invalid command")
        # Execute the function
        return func()

