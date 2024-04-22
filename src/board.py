#!/usr/bin/env python3

import json

from src.board_header.mcp23017_h import BoardMCP23017, I2c_obj


class BoardConfig:
    def __init__(self, config_file: str = None) -> None:
        self.config = None
        self.config_file = config_file

        self.i2c_obj = I2c_obj()

        self.boards = {}

        self.load_config()

    def create_boards(self):
        for board in self.config["boards"]:
            self.boards[board["name"]] = BoardMCP23017(
                name=board["name"],
                address=board["address"],
                i2c_obj=self.i2c_obj,
            )

    def load_config(self, config_file: str = None):
        # TODO: maybe this can call all the other functions to refresh runtime
        self.config_file = config_file if config_file else self.config_file
        with open(self.config_file, 'r') as file:
            self.config = json.load(file)
