from typing import Any


class EmulatedSMBus:
    def __init__(self):
        """
        this is a very primitive smbus emulation to let i2c modules think
        they are talking to something real
        """
        # this dict just has bytes stored at addresses
        self._data: dict = dict()
        self._address = None

    def _check_addr(self):
        """
        some wrapper
        :return:
        """
        pass

    def write_byte_data(self, address: bytes, offset: bytes, value: bytes) -> None:
        print(offset)
        print(value)
        self._data[offset] = value

    def read_byte(self, address: bytes) -> dict[bytes, bytes]:
        # TODO: need to fill up till some level
        return self._data

    def read_byte_data(self, address: bytes, offset: bytes) -> int:
        """

        :param address:
        :param offset:
        :return:
        """
        print(offset)
        if offset in self._data:
            return self._data[offset]
        # we have to make sure we return something
        return 0


class VirtualMCP23017:
    pass
