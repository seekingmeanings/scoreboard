#!/usr/bin/env python3

import tomlkit

from board_header.mcp23017_h import BoardMCP23017

from activator import LED


class BoardConfig:
    def __init__(self, config_file: str = None) -> None:
        self.digits = None
        self.boards = None
        self.config = None
        self.config_file = config_file

        self.load_config()
        self.create_structure()

    def create_boards(self):
        self.boards = dict()
        for board in self.config["boards"]:
            # TODO: assign right board type (need to finish the resource stuff)
            self.boards[board] = BoardMCP23017(
                name=board,
                address=self.config["boards"][board]["address"],
            )

    def create_structure(self):
        self.create_boards()
        # create and link the leds
        self.digits = dict()
        for segment_group in self.config["activator"]:
            for segment in self.config["activator"][segment_group]:
                self.digits[segment["id"]] = None
                for connection in segment["connections"]:
                    brd, gpio = str(segment["connections"][connection]).split(".")
                    self.digits[segment["id"]][connection] = \
                        LED(
                            io_link=self.boards[brd].get_board_obj(),
                            pin=gpio,
                            name=connection,
                            constants=self.boards[brd].stupid_place_to_put_consts_ffs
                        )

    def load_config(self, config_file: str = None):
        # TODO: maybe this can call all the other functions to refresh runtime
        self.config_file = config_file if config_file else self.config_file
        with open(self.config_file, 'r') as file:
            self.config = tomlkit.load(file)


if __name__ == "__main__":
    bc = BoardConfig("board_layout.toml")
