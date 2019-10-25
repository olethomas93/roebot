from pyModbusTCP.client import ModbusClient
import time
from threading import Thread, Lock
from pyModbusTCP import utils

SERVER_HOST = "158.38.140.61"
SERVER_PORT = 2000

# set global
regs = []

# init a thread lock
regs_lock = Lock()

class modbusClient(object):

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

    # modbus polling thread
    def polling_thread(self):
        global regs
        c = ModbusClient(host=SERVER_HOST, port=SERVER_PORT)
        # polling loop
        while True:
            # keep TCP open
            if not c.is_open():

                c.open()
            # do modbus reading on socket




            reg_list = c.read_holding_registers(0, 20)
            # if read is ok, store result in regs (with thread lock synchronization)
            if reg_list:
                with regs_lock:
                    regs = list(reg_list)
                    for x in regs:
                        print(x)



            # 1s before next polling
            time.sleep(3)


    # start polling thread
    tp = Thread(target=polling_thread )
    # set daemon: polling thread will exit if main thread exit
    tp.daemon = True
    tp.start()

    # display loop (in main thread)
    while True:
        # print regs list (with thread lock synchronization)
        with regs_lock:
            print(regs[1])
        # 1s before next print
        time.sleep(1)
