import os

import time

from src.things.scoreboard.scoreboard import Scoreboard

from typing import Optional
import logging

import tomllib


class TimePlugin:
    # TODO: move ConfigLoader and other parents to common plugin parent
    def __init__(self, board: Scoreboard, config_file: str):
        self.lg = logging.getLogger(self.__class__.__name__)
        # TODO: use Config class
        self.config: dict = dict()
        self.config_file: str = os.path.join(os.path.dirname(__file__), config_file)
        with open(self.config_file, 'rb') as f:
            self.config = tomllib.load(f)

        self.lg.debug(f"loaded config: {self.config} from {self.config_file}")

        # linked board resource
        self.board: Scoreboard = board

        self._time: Optional[time.struct_time] = None
        self._active: bool = False
        self._alive = False

        self._custom_time = None

    def _clear(self):
        for digit_name, digit_obj in self.config["digits"].items():
            self.board.display_char(digit_name, None)


    def set_time(self, time_to_set: time.struct_time) -> None:
        self.lg.debug(f"setting time to {time_to_set}")
        for digit_name, digit_obj in self.config["digits"].items():
            format_str, index = (digit_obj["strftime"]["format"],
                                 digit_obj["strftime"]["index"])
            char = str(time.strftime(format_str, time_to_set))[index]
            self.board.display_char(digit_name, char)

    def set_custom_time(self, time_to_set: time.struct_time) -> None:
        # TODO: implement custom time setting
        self.lg.debug(f"setting custom time to {time_to_set}")
        raise NotImplementedError()

    def update_time(self):
        while self._alive:
            if not self._active:
                continue

            # TODO: apply custom time
            last = time.localtime()
            while self._active:
                now = time.localtime()
                if time.mktime(now) - time.mktime(last) >= 1:
                    self.set_time(now)
                    last = now
                time.sleep(float(self.config['time']["update_interval"])/1000)
            self._clear()


        self.lg.warning("time update loop stopped")

    def display_time_toggle(self):
        self._active = not self._active

    @property
    def display_time(self):
        if self._alive:
            return {'active': self._active}
        return False

    @display_time.setter
    def display_time(self, state: bool):
        if self._alive:
            self._active = state
        else:
            raise RuntimeError("The thread is dead")

    def run(self):
        # TODO: proper on and off function
        self._alive = True
        self._active = True

        # make sure its declare dead
        try:
            self.update_time()
        finally:
            self._alive = False

    def stop(self):
        self._active = False
