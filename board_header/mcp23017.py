# only pi specific, needs to be flagged

import mcp23017 as mcp
import smbus

from board_header.board import Board


class BoardMCP23017(Board):
    type = "mcp23017"

    # TODO: get pin stuff as obj....

    def __init__(self, name: str, address: str) -> None:
        super().__init__(name=name, address=address)

        self.io_link = mcp.MCP23017(
            address=self.address,
            smbus=smbus.SMBus(1)
        )

        self.stupid_place_to_put_consts_ffs = mcp
        self.gpio = mcp.ALL_GPIO


# resource_interface