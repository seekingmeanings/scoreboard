#!/usr/bin/env python3

# only pi specific, needs to be flagged
import mcp23017 as mcp
from i2c import I2C
import smbus



import json
from activator import ExtenderBoard

class Board:
    def __init__(self) -> None:
        pass

    class Segment:
        def __init__(self) -> None:
            pass


class BoardConfig:
    def __init__(self, config_file: str) -> None:
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> dict:
        with open(self.config_file, 'r') as file:
            return json.load(file)
        
    def _get_board(self) -> Board:
        for board in self.boards:
            if board['type'] not in self.config['outputs']:
                raise ValueError(f'Board type {board["type"]} not found in config')
            lol = self.config['boards']



    def get_led(self, led_id: int) -> LED:
        led = self.config['leds'][led_id]
        return LED(led['pin'], led['color'])

    def get_segment(self, segment_id: int) -> Board.Segment:
        segment = self.config['segments'][segment_id]
        return Board.Segment()