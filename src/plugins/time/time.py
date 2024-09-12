import os

import time
import asyncio

from typing import Optional
import logging as lg

import tomllib


class TimePlugin:
    # TODO: get the board linker to link outside of the class for all once \
    # TODO: and then populate classes like this with (classwrapper???)

    # TODO: move ConfigLoader and other parents to common plugin parent
    def __init__(self, board, config_file: str):
        # TODO: use Config class
        self.config: dict = dict()
        self.config_file: str = os.path.join(os.path.dirname(__file__), config_file)
        with open(self.config_file, 'rb') as f:
            self.config = tomllib.load(f)

        print(f"loaded config: {self.config} from {self.config_file}")

        # linked board resource
        self.board = board

        self._time: Optional[time.struct_time] = None
        self._active: bool = False

    def set_time(self, time_to_set: time.struct_time) -> None:
        lg.debug(f"setting time to {time_to_set}")
        for digit_name, digit_obj in self.config["digits"].items():
            format_str, index = (digit_obj["strftime"]["format"],
                                 digit_obj["strftime"]["index"])
            char = str(time.strftime(format_str, time_to_set))[index]
            self.board.display_char(digit_name, char)

    def update_time(self):
        last = time.gmtime()
        while self._active:
            now = time.gmtime()
            if time.mktime(now) - time.mktime(last) >= 1:
                self.set_time(now)
                last = now
            time.sleep(float(self.config['time']["update_interval"])/1000)

        lg.debug("time update loop stopped??")

    def run(self):
        self._active = True
        self.update_time()

    def stop(self):
        self._active = False
