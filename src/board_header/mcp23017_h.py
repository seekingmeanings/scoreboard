# only pi specific, needs to be flagged

import mcp23017 as mcp
import smbus


class Board:
    def __init__(self, name, address):
        self.name = name
        self.address = address

        self.io_link: object = None

    def get_board_obj(self):
        return self.io_link


class BoardMCP23017(Board):
    type = "mcp23017"

    # TODO: get pin stuff as obj....

    def __init__(self, name: str, address: str) -> None:
        super().__init__(name=name, address=address)

        self.io_link = mcp.MCP23017(
            address=self.address,
            smbus=smbus.SMBus(1)
        )

        self.gpio = mcp.ALL_GPIO


# resource_interface