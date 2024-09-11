from src.helper.race_condition import LockedTracking
from typing import Any, List, Dict, Union
import os


class Config(LockedTracking):
    def __init__(self, config_file: str) -> None:
        super().__init__()
        self._config_file = config_file

        # load the config file
        self._config = None
        self._load()

    def _load(self) -> None:
        """
        load the config file

        if an edited version exists, load it instead
        :return:
        """
        if os.path.exists(self._config_file + ".edited"):
            with open(self._config_file + ".edited", "r") as f:
                self._config = f.read()
        else:
            with open(self._config_file, "r") as f:
                self._config = f.read()

    def update(self) -> None:
        """
        reload the config file itself
        :return:
        """
        pass

    @LockedTracking.locked_access
    def get(self) -> Any:
        """
        get the config stack
        :return:
        """
        return self._config

    @LockedTracking.locked_access
    def set(self):
        """
        set a value in the config stack

        after that, the config file will be updated
        there will be a new file with the ending .edited
        that will be loaded instead of the original file
        to not overwrite the original file
        :return:
        """
        pass
