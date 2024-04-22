# only pi specific, needs to be flagged

import mcp23017 as mcp

from i2c import I2C
import smbus


class I2c_obj:
    def __init__(self):
        self.obj = I2C(smbus.SMBus(1))


class BoardMCP23017:
    type = "mcp23017"

    def __init__(self, name: str, address: str, i2c_obj) -> None:
        self.name = name
        self.i2c_obj = i2c_obj
        self.address = address

        self.board = mcp.MCP23017(self.address, self.i2c_obj)

    def get_board_obj(self) -> mcp.MCP23017:
        return self.board

# resource_interface
