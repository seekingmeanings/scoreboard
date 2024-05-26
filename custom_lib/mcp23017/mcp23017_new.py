from dataclasses import dataclass

import smbus


class I2C:
    def __init__(self, smbus_num: int = 1) -> None:
        # make it not close on exit

        self.sbus = smbus.SMBus(smbus_num)

    def write(self, address: hex, offset: hex, value: hex) -> None:
        self.sbus.write_byte_data(address, offset, value)

    def read(self, address, register=None):
        return self.sbus.read_byte_data(address, register) if register \
            else self.sbus.read_byte(address)


@dataclass(frozen=True)
class HexVal:
    class Register:
        IODIRA = 0x00  # Pin direction register
        IODIRB = 0x01  # Pin direction register
        IPOLA = 0x02
        IPOLB = 0x03
        GPINTENA = 0x04
        GPINTENB = 0x05
        DEFVALA = 0x06
        DEFVALB = 0x07
        INTCONA = 0x08
        INTCONB = 0x09
        IOCONA = 0x0A
        IOCONB = 0x0B
        GPPUA = 0x0C
        GPPUB = 0x0D

        INTFA = 0x0E
        INTFB = 0x0F
        INTCAPA = 0x10
        INTCAPB = 0x11
        GPIOA = 0x12
        GPIOB = 0x13
        OLATA = 0x14
        OLATB = 0x15

    class IO:
        GPA0 = 0
        GPA1 = 1
        GPA2 = 2
        GPA3 = 3
        GPA4 = 4
        GPA5 = 5
        GPA6 = 6
        GPA7 = 7
        GPB0 = 8
        GPB1 = 9
        GPB2 = 10
        GPB3 = 11
        GPB4 = 12
        GPB5 = 13
        GPB6 = 14
        GPB7 = 15

    HIGH = 0xFF
    LOW = 0x00

    INPUT = 0xFF
    OUTPUT = 0x00

class MCP23017:
    def __init__(self, i2c: I2C, address):
        self.i2c = i2c
        self.address = address

    def set_mode(self, mode, gpio=None):
        if gpio:
            # mask things
            return
        for reg in (HexVal.Register.IODIRA, HexVal.Register.IODIRB):
            self.i2c.write(self.address, reg, mode)

			# make write funtion for single bit and write entire bit addr??
			# way fastwr this way, dont have to get tbe stuff and mask it
			# its just one io op then

