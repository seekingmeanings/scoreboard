#!/usr/bin/env python3

import tomlkit
import logging as lg
from src.board_header.mcp23017_h import BoardMCP23017

from src.things.activator import LED


class BoardConfig:
    def __init__(self, chiffres_config_file: str, board_config_file: str = None) -> None:
        self.digits = None
        self.boards = None
        self.config = None
        self.chiffres = dict()
        self.board_config_file = board_config_file
        self.chiffres_config_file = chiffres_config_file

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

    def setup_chiffres(self):
        for number in self.chiffres_config["numbers"]:
            self.chiffres[int(number)] = set(self.chiffres_config["numbers"][number])

    def create_structure(self):
        self.create_boards()
        # create and link the leds
        self.digits = dict()
        for segment_group in self.config["activator"]:
            for segment in self.config["activator"][segment_group]:
                self.digits[segment["id"]] = {}
                for connection in segment["connections"]:
                    brd, gpio = str(segment["connections"][connection]).split(".")
                    self.digits[segment["id"]][connection] = \
                        LED(
                            io_link=self.boards[brd].get_board_obj(),
                            pin=gpio,
                            name=connection,
                            constants=self.boards[brd].stupid_place_to_put_consts_ffs
                        )

    def load_config(self, board_config_file: str = None, chiffres_config_file: str = None):
        # TODO: maybe this can call all the other functions to refresh runtime
        self.board_config_file = board_config_file if board_config_file else self.board_config_file
        self.chiffres_config_file = chiffres_config_file if chiffres_config_file else self.chiffres_config_file

        with open(self.board_config_file, 'r') as file:
            self.config = tomlkit.load(file)

        with open(self.chiffres_config_file, 'r') as file:
            self.chiffres_conf = tomlkit.load(file)
            self.chiffres = self.chiffres_conf["numbers"]

    def display_char(self, digit_id, character: str | int = None):
        if type(character) == str:
            if not len(character) == 1:
                raise OverflowError(f"only one character is allowed, got {character}")

        lg.debug(f"{digit_id}: {character}")

        try:
            # buffer the digit access
            digit = self.digits[digit_id]

            if character is None:
                # TODO: geht nihcts
                lg.debug(f"{digit} going dark")
                for led in digit:
                    digit[led].off()
                print("lol")
                return

            character = str(character)

            lg.debug(f"{digit}")
            off_chars = (set(self.chiffres_conf["other"]["all"]) - set(self.chiffres[character]))
            lg.debug(f"{off_chars}")

            # activate the leds
            if type(character) is str:
                for led in self.chiffres[character]:
                    digit[led].on()

                for led in off_chars:
                    digit[led].off()

            else:
                raise NotImplementedError()

        except KeyError as e:
            raise ValueError(
                f'the character "{character}" {type(character)}is not in {self.chiffres_config_file}'
            ) from e

        except Exception as e:
            raise RuntimeError from e

    def get_board_state(self) -> list[any]:
        ret = {}
        for digit in self.digits:
            lg.debug(digit)
            ret[digit] = {}
            for led in self.digits[digit]:
                ret[digit][led] = self.digits[digit][led].state

        return ret