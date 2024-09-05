#!/usr/bin/env python3

import tomlkit
import logging as lg
# TODO: make self overlay of the lib that supports both with a flag
from board_header.mcp23017 import BoardMCP23017
from board_header.virtual_mcp23017 import VirtualMCP23017

from src.things.activator import LED


class Scoreboard:
    """
    This class is the data class that modifies
    the actual scoreboard
    """
    # TODO: clean up the stupid dict for iters
    def __init__(
            self, character_config_file: str,
            board_config_file: str = None,
            virtual: bool = False,
    ) -> None:
        self.virtual: bool = virtual
        self.digits = None
        self.boards: dict = dict()
        self.config: dict = None
        self.character = dict()
        self.board_config_file = board_config_file
        self.character_config_file = character_config_file

        self.load_config()
        self.create_structure()

    def create_boards(self):
        # TODO: this has to go somewhere else, this class should not be specific
        # TODO: or maybe the functions dont belong to this class
        for board_name, board_obj in self.config["boards"].items():
            # TODO: assign right board type (need to finish the resource stuff)
            if self.virtual:
                self.boards[board_name] = VirtualMCP23017(
                    name=board_name,
                    address=board_obj["address"]
                )
                continue

            self.boards[board_name] = BoardMCP23017(
                name=board_name,
                address=board_obj["address"],
            )

    def setup_characters(self):
        # TODO: why isnt that called??
        for number in self.characters_conf["numbers"]:
            self.character[int(number)] = set(self.characters_conf["numbers"][number])

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

    def load_config(self, board_config_file: str = None, characters_config_file: str = None):
        # TODO: maybe this can call all the other functions to refresh runtime
        self.board_config_file = board_config_file if board_config_file else self.board_config_file
        self.character_config_file = characters_config_file if characters_config_file else self.character_config_file

        with open(self.board_config_file, 'r') as file:
            self.config = tomlkit.load(file)

        with open(self.character_config_file, 'r') as file:
            self.characters_conf = tomlkit.load(file)
            self.character = self.characters_conf["numbers"]

    def display_char(self, digit_id, character: str | int = None):
        if type(character) == str:
            if not len(character) == 1:
                raise OverflowError(f"only one character is allowed, got {character}")

        lg.debug(f"{digit_id}: {character}")

        try:
            # buffer the digit access
            digit = self.digits[digit_id]

            # set everything off
            if character is None:
                # TODO: geht nihcts
                lg.debug(f"{digit} going dark")
                for led in digit:
                    digit[led].off()
                print("lol")
                return

            character = str(character)

            lg.debug(f"{digit}")
            off_chars = (set(self.characters_conf["other"]["all"]) - set(self.character[character]))
            lg.debug(f"{off_chars}")

            # activate the leds
            if type(character) is str:
                for led in self.character[character]:
                    digit[led].on()

                for led in off_chars:
                    digit[led].off()

            else:
                raise NotImplementedError()

        except KeyError as e:
            raise ValueError(
                f'the character "{character}" {type(character)}is not in {self.character_config_file}'
            ) from e

        except Exception as e:
            raise RuntimeError from e

    def get_board_state(self) -> dict[str, dict[str, bool]]:
        """
        Retrieve the current state of the board as a dictionary
        containing the digits as the keys, and as vals
        another dictionary containing dicts of led_id str and the state
        :return:
        """
        ret = {}
        for digit in self.digits:
            ret[digit] = {}
            for led in self.digits[digit]:
                ret[digit][led] = self.digits[digit][led].state

        # return ret

        return {
            digit: {led: led_obj.state for led, led_obj in leds.items()}
            for digit, leds in self.digits.items()
        }
