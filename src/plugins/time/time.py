from src.helper.conf_loader import ConfigLoader
from src.helper.board_linker import BoardLinker

from public import public
import time
import asyncio

import logging as lg


class TimePlugin(ConfigLoader, BoardLinker):
    # TODO: get the board linker to link outside of the class for all once \
    # TODO: and then populate classes like this with (classwrapper???)

    # TODO: move ConfigLoader and other parents to common plugin parent
    def __init__(self, board, config_file: str):
        ConfigLoader.__init__(self, config_file)
        # TODO: some better dynamic linking
        BoardLinker.__init__(self, board=board)
        self._time = None
        self._active = True

    @public
    def set_time(self, time_to_set: time.struct_time) -> None:
        for digit_name, digit_obj in self.config["digits"].items():
            format_str, index = (digit_obj["strftime"]["format"],
                                 digit_obj["strftime"]["index"])
            char = str(time.strftime(format_str, time_to_set))[index]
            self.board.display_char(digit_name, char)
            lg.debug(f"setting time component: {digit_name}: {char}")

    async def update_time(self):
        last = time.gmtime()
        while self._active:
            now = time.gmtime()
            if time.mktime(now) - time.mktime(last) >= 1:
                self.set_time(now)
                last = now
            await asyncio.sleep(self.config["update_interval"])

    @public
    def run(self):
        asyncio.run(self.update_time())
