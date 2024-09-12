from board_header.board import Board
import mcp23017 as mcp

import logging as lg

class EmulatedSMBus:
    def __init__(self):
        """
        this is a very primitive smbus emulation to let i2c modules think
        they are talking to something real
        """
        # this dict just has bytes stored at addresses
        self._data: dict = dict()
        self._address = None

        self.logger = lg.getLogger("EmulatedSMBus")

    def _check_addr(self):
        """
        some wrapper
        :return:
        """
        pass

    def write_byte_data(self, address: hex, offset: int, value: hex) -> None:
        """
        write at an offset
        :param address: GPIO to OLAT write through
        :param offset:
        :param value:
        :return:
        """
        self.logger.debug(f"write at {hex(offset)}: {hex(value)}")
        self._data[offset] = value

    def read_byte(self, address: bytes) -> dict[bytes, bytes]:
        # TODO: need to fill up till some level
        return self._data

    def read_byte_data(self, address: bytes, offset: int) -> int:
        """

        :param address:
        :param offset:
        :return:
        """
        self.logger.debug(f"reading from {hex(offset)}: {hex(self._data[offset]) if offset in self._data else hex(0)}")
        if offset in self._data:
            return self._data[offset]
        # we have to make sure we return something
        return 0


class EmulatedSMBusMCP23017(EmulatedSMBus):
    def write_byte_data(self, address: hex, offset: int, value: hex) -> None:
        super().write_byte_data(address, offset, value)

        o_lat = offset - 2
        if o_lat in {0x12, 0x13}:
            super().write_byte_data(address, o_lat, value)


class VirtualMCP23017(Board):
    type = "mcp23017"

    def __init__(self, name: str, address: str) -> None:
        super().__init__(name=name, address=address)
        self.io_link = mcp.MCP23017(
            address=self.address,
            smbus=EmulatedSMBusMCP23017()
        )

        self.stupid_place_to_put_consts_ffs = mcp
        self.gpio = mcp.ALL_GPIO

# TODO: resource interface
