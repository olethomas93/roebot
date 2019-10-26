from pyModbusTCP.client import ModbusClient
import time
from threading import Thread, Lock
from pyModbusTCP import utils

# set global
regs = []

# init a thread lock
regs_lock = Lock()



class modbusClient(object):
    th = None

    def __init__(self):
        self.th = Thread(target=self.polling_thread, args=())
        self.SERVER_HOST = "169.254.127.11"
        self.SERVER_PORT = 2000

    def read_float(self, address, number=1):
        reg_l = self.read_holding_registers(address, number * 2)
        if reg_l:
            return [utils.decode_ieee(f) for f in utils.word_list_to_long(reg_l)]
        else:
            return None

    def write_float(self, address, floats_list):
        b32_l = [utils.encode_ieee(f) for f in floats_list]
        b16_l = utils.long_list_to_word(b32_l)
        return self.write_multiple_registers(address, b16_l)

    def getValue(self,address):
        self.th.daemon = True
        self.th.start()
        while True:
            # print regs list (with thread lock synchronization)
            with regs_lock:
                if len(regs)>0:


                    if  regs[address] == 34:
                        return True


            # 1s before next print
            time.sleep(1)


    # modbus polling thread
    def polling_thread(self):
        global regs

        c = ModbusClient(host=self.SERVER_HOST, port=self.SERVER_PORT)
        # polling loop
        while True:

            # keep TCP open
            if not c.is_open():
                if not c.open():
                    print("unable to connect to " + self.SERVER_HOST + ":" + str(self.SERVER_PORT))

            # do modbus reading on socket
            if c.is_open():
                print("connection")
                reg_list = c.read_holding_registers(0, 10)
                # if read is ok, store result in regs (with thread lock synchronization)
                if reg_list:
                    with regs_lock:
                        regs = reg_list

                # 1s before next polling
                time.sleep(1)



