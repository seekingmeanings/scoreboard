import pytest
from unittest.mock import MagicMock, patch
from src.things.scoreboard.scoreboard import Scoreboard, Digit, LED

def test_create_structure_creates_correct_digits():
    scoreboard = Scoreboard(character_config_file='path/to/character_config.toml', board_config_file='path/to/board_config.toml')
    scoreboard.config = {
        "boards": {
            "board1": {"address": 0x20}
        },
        "activator": {
            "segment1": [
                {"id": "digit0", "type": "type1", "connections": {"A": "board1.0", "B": "board1.1"}}
            ]
        }
    }
    scoreboard.create_boards = MagicMock()
    scoreboard.create_structure()
    assert "digit0" in scoreboard.digits
    assert "A" in scoreboard.digits["digit0"].connections
    assert "B" in scoreboard.digits["digit0"].connections

def test_display_char_turns_off_all_leds_when_character_is_none():
    scoreboard = Scoreboard(character_config_file='path/to/character_config.toml', board_config_file='path/to/board_config.toml')
    scoreboard.digits = {
        "digit0": Digit(id="digit0", connections={"A": MagicMock(), "B": MagicMock()})
    }
    scoreboard.display_char("digit0", None)
    scoreboard.digits["digit0"].connections["A"].off.assert_called_once()
    scoreboard.digits["digit0"].connections["B"].off.assert_called_once()

def test_display_char_raises_value_error_for_invalid_character():
    scoreboard = Scoreboard(character_config_file='path/to/character_config.toml', board_config_file='path/to/board_config.toml')
    scoreboard.character = {"1": {"A", "B"}}
    with pytest.raises(ValueError):
        scoreboard.display_char("digit0", "invalid_char")

def test_display_char_raises_overflow_error_for_multiple_characters():
    scoreboard = Scoreboard(character_config_file='path/to/character_config.toml', board_config_file='path/to/board_config.toml')
    with pytest.raises(OverflowError):
        scoreboard.display_char("digit0", "AB")

def test_display_char_turns_on_correct_leds_for_character():
    scoreboard = Scoreboard(character_config_file='path/to/character_config.toml', board_config_file='path/to/board_config.toml')
    scoreboard.digits = {
        "digit0": Digit(id="digit0", connections={"A": MagicMock(), "B": MagicMock(), "C": MagicMock()})
    }
    scoreboard.character = {"1": {"A", "B"}}
    scoreboard.characters_conf = {"other": {"all": {"A", "B", "C"}}}
    scoreboard.display_char("digit0", "1")
    scoreboard.digits["digit0"].connections["A"].on.assert_called_once()
    scoreboard.digits["digit0"].connections["B"].on.assert_called_once()
    scoreboard.digits["digit0"].connections["C"].off.assert_called_once()