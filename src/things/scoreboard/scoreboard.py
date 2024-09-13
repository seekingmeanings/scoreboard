from dataclasses import dataclass
from typing import List, Dict, Union
import tomlkit
import logging as lg
# TODO: make self overlay of the lib that supports both with a flag
from board_header.mcp23017 import BoardMCP23017
from board_header.virtual_mcp23017 import VirtualMCP23017

from src.things.activator import LED

from .digits import Digit


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
        self.digits: Dict[str, Scoreboard.Digit] = {}
        self.boards: dict = {}
        self.config: dict = None
        self.character = {}
        self.board_config_file = board_config_file
        self.character_config_file = character_config_file
        self.segments: dict = {}

        self.characters_conf = None

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
        # TODO: this should be in the digit class not here
        for segment_name in self.config["activator"]:
            self.segments[segment_name] = []
            for digit in self.config["activator"][segment_name]:
                new_digit = Digit(id=digit["id"], type=digit['type'], connections={})
                self.digits[digit["id"]] = new_digit
                for connection in digit["connections"]:
                    brd, gpio = str(digit["connections"][connection]).split(".")

                    new_led = \
                        LED(
                            io_link=self.boards[brd].get_board_obj(),
                            pin=gpio,
                            name=connection,
                            constants=self.boards[brd].stupid_place_to_put_consts_ffs
                        )
                    self.digits[digit["id"]].connections[connection] = new_led
                self.segments[segment_name].append(new_digit)

    def load_config(self, board_config_file: str = None, characters_config_file: str = None):
        # TODO: maybe this can call all the other functions to refresh runtime
        self.board_config_file = board_config_file if board_config_file else self.board_config_file
        self.character_config_file = characters_config_file if characters_config_file else self.character_config_file

        with open(self.board_config_file, 'r') as file:
            self.config = tomlkit.load(file)

        with open(self.character_config_file, 'r') as file:
            self.characters_conf = tomlkit.load(file)
            # TODO: outdated, update class to new config file format
            self.character = self.characters_conf['7segment']["numbers"]

    def to_dots(self, digit: Union[Digit, Dict] = None, digit_type: str = None) -> Dict:
        """
        convert the io to a list of dots

        this can be used to display the dots on the scoreboard
        :param digit: the digit to convert, can be list of io, then digit_type is needed
        :param digit_type: the type of the digit, if none, it will be looked up with the digit id
        :return:
        """
        # return everything in self.digits
        # TODO: not use that
        if not digit:
            digit = {
                digit_name: self.digits[digit_name].connections
                for digit_name in self.digits
            }

        if digit_type is None:
            # check if its a digit object or a list
            if isinstance(digit, Digit):
                digit = digit.connections
                digit_type = digit.type
            else:
                return {
                    digit_name: self.to_dots(
                        io_stuff,
                        self.digits[digit_name].type
                    )
                    for digit_name, io_stuff in digit.items()
                }
        # TODO: other input cases

        res = {}
        for io_name, io_obj in digit.items():
            io_state = io_obj.state if isinstance(io_obj, LED) else io_obj
            for dots in self.characters_conf[digit_type]['dots']['io_to_dot'][io_name]:
                for dot in dots:
                    res[dot] = io_state
        return res

    def from_dots(self, dots: List) -> List:
        pass

    def display_char(self, digit_id, character: Union[str, int, None] = None):
        if isinstance(character, str):
            if not len(character) == 1:
                raise OverflowError(f"only one character is allowed, got {character}")

        lg.debug(f"{digit_id}: {character}")

        # TODO: put lots of that in the Digit class itself
        try:
            # buffer the digit access
            digit = self.digits[digit_id]

            # set everything off
            if character is None:
                # TODO: geht nihcts
                lg.debug(f"{digit} going dark")
                for led in digit.connections:
                    digit.connections[led].off()
                return

            character = str(character)

            lg.debug(f"{digit}")

            off_chars = (
                    set(self.characters_conf[digit.type]["other"]["all"])
                    - set(self.characters_conf[digit.type]["numbers"][character])
            )
            lg.debug(f"{off_chars}")

            # activate the leds
            if type(character) is str:
                for led in self.character[character]:
                    digit.connections[led].on()

                for led in off_chars:
                    digit.connections[led].off()

            else:
                raise NotImplementedError()

        except KeyError as e:
            raise ValueError(
                f'the character "{character}" {type(character)}is not in {self.character_config_file}'
            ) from e
