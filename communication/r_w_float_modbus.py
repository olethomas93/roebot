#!/usr/bin/env python
# -*- coding: utf-8 -*-

# how-to add float support to ModbusClient

from pyModbusTCP import utils


class FloatModbusClient():

    def __init__(self,Modbus):
        self.ModbusClient = Modbus
        self.reg_l = []

    def read_float(self, address, number=1):
        self.reg_l = self.ModbusClient.read_holding_registers(address, number * 1)
        if self.reg_l:
            return self.reg_l, False
        else:
            return 0, True

    def write_float(self, address, floats_list):
        b32_l = [utils.encode_ieee(f) for f in floats_list]
        b16_l = utils.long_list_to_word(b32_l)
        return self.ModbusClient.write_multiple_registers(address, b16_l)
