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
        """Send a 32 bit value to the first modbus unit.
        Parameters: value and address where the value will be
        stored in.
        Return: Result if it was successful or not."""
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_32bit_int(value)
        payload = builder.build()
        result = self.modbusClient.write_registers(address, payload, skip_encode=True, unit=1)
        return result

    def write_float(self, address, value):

        b16_l = utils.long_list_to_word(value)

        return self.modbusClient.write_multiple_registers(address, b16_l)
