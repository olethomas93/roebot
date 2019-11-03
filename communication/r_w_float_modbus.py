#!/usr/bin/env python
# -*- coding: utf-8 -*-

# how-to add float support to ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils


class FloatModbusClient():

    def __init__(self, modbus):
        self.modbusClient = modbus(host="158.38.140.52", port=2000, auto_open=True)
        self.reg_l = []

    def read_float(self, address, number=1):
        self.reg_l = self.modbusClient.read_holding_registers(address, number * 1)
        if self.reg_l:
            return self.reg_l, False
        else:
            return 0, True

    def sendInt(self, value, address):

        result = self.modbusClient.write_single_register(address, value)
        return result

    def write_float(self, address, floats_list):
        b32_l = [utils.encode_ieee(f) for f in floats_list]
        b16_l = utils.long_list_to_word(b32_l)
        return self.modbusClient.write_multiple_registers(address, floats_list)