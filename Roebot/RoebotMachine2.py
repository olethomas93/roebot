from pyModbusTCP.client import ModbusClient
import time
from threading import Thread, Lock
from ImageProcessing import Coordinate, singleMotionDetector
from ImageProcessing import Camera
from ImageProcessing import imageProcessing2
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
from imutils.video import VideoStream
import datetime
import imutils
import time
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

SERVER_HOST = "192.168.137.65"
SERVER_PORT = 2000

# init a thread lock
regs_lock = Lock()
outputFrame = None
lock = Lock()

vs = VideoStream(usePiCamera=0).start()
time.sleep(2.0)
# initialize a flask object
app = Flask()


class roebot():

    def __init__(self, threadpool):
        self.tp = Thread(target=self.polling_thread)
        self.th = Thread(target=self.detect_motion, args=(32,))
        self.threadpool = threadpool
        self.regList = []
        self.tp.start()
        self.th.daemon = True
        self.th.start()
        self.pictureIndex = 0
        self.camera = Camera.Camera()
        self.imageCv = imageProcessing2.imageProcessing()
        self.imageList = []
        app.run(host="localhost", port="8080", debug=True,
                threaded=True, use_reloader=False)

        # self.modbusclient = r_w_float_modbus.FloatModbusClient(ModbusClient)

    def poll_command(self):
        print("Polling server for commands")
        commandpoll = False
        # display loop (in main thread)
        while not commandpoll:

            # print regs list (with thread lock synchronization)

            if self.regList:
                command = self.regList[0]
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

            if len(list) > 0:

                for i in range(len(list)):
                    coordinate = list[i]

                    xpos = coordinate.getxCoor() + ((int(roeImage.getPictureIndex()) + 1) * 300)
                    ypos = coordinate.getyCoor()

                    newcoord = Coordinate.coordinate(xpos, ypos)

                    coordList.append(newcoord)

        return coordList

    def sendCordToPLC(self):
        print("sending to PLC")
        arrayX = []
        arrayY = []
        corrdList = self.generatecoordinateList()
        for cord in corrdList:
            arrayX.append(cord.getxCoor())
            arrayY.append(cord.getyCoor())
        print(arrayX)
        self.client.write_multiple_registers(10, arrayX)

        # sleep so register can be updated
        time.sleep(1)
        self.imageCv.processingQueue = []
        self.imageList = []
        self.switch_case(0)

    def getImageList(self):
        print(len(self.imageList))
        time.sleep(1)
        self.switch_case(0)

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

    @app.route("/")
    def index(self):
        # return the rendered template
        return render_template("index.html")

    def detect_motion(self, frameCount):
        # grab global references to the video stream, output frame, and
        # lock variables
        global vs, outputFrame, lock

        # initialize the motion detector and the total number of frames
        # read thus far
        md = singleMotionDetector.SingleMotionDetector(accumWeight=0.1)
        total = 0
        # loop over frames from the video stream
        # loop over frames from the video stream
        while True:
            # read the next frame from the video stream, resize it,
            # convert the frame to grayscale, and blur it
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)

            # grab the current timestamp and draw it on the frame
            timestamp = datetime.datetime.now()
            cv2.putText(frame, timestamp.strftime(
                "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            # if the total number of frames has reached a sufficient
            # number to construct a reasonable background model, then
            # continue to process the frame
            if total > frameCount:
                # detect motion in the image
                motion = md.detect(gray)

                # check to see if motion was found in the frame
                if motion is not None:
                    # unpack the tuple and draw the box surrounding the
                    # "motion area" on the output frame
                    (thresh, (minX, minY, maxX, maxY)) = motion
                    cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                                  (0, 0, 255), 2)

                # update the background model and increment the total number
                # of frames read thus far
            md.update(gray)
            total += 1

            # acquire the lock, set the output frame, and release the
            # lock
            with lock:
                outputFrame = frame.copy()

    def generate(self):
        # grab global references to the output frame and lock variables
        global outputFrame, lock

        # loop over frames from the output stream
        while True:
            # wait until the lock is acquired
            with lock:
                # check if the output frame is available, otherwise skip
                # the iteration of the loop
                if outputFrame is None:
                    continue

                # encode the frame in JPEG format
                (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

                # ensure the frame was successfully encoded
                if not flag:
                    continue

            # yield the output frame in the byte format
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(encodedImage) + b'\r\n')

    @app.route("/video_feed")
    def video_feed(self):
        # return the response generated along with the specific media
        # type (mime type)
        return Response(self.generate(),
                        mimetype="multipart/x-mixed-replace; boundary=frame")

    vs.stop()
