from src.helper.race_condition import LockedTracking
from typing import Any, List, Dict, Union
import os
import tomlkit
import logging


class Config(LockedTracking):
    def __init__(self, config_file: str) -> None:

        super().__init__()

        self.lg = logging.getLogger(__name__)

        self.edited_affix = ".edited"
        self._config_file = config_file
        self._edited_fp = self._config_file + self.edited_affix

        # load the config file
        self._config = None
        self.reload()

    def reload(self) -> None:
        """
        load the config file

        if an edited version exists, load it instead
        :return:
        """
        if os.path.exists(self._edited_fp):
            with open(self._edited_fp, "r") as f:
                self.lg.info(f"loading config as toml from: {self._edited_fp}")
                self._config = tomlkit.load(f)

        else:
            with open(self._config_file, "r") as f:
                self.lg.info(f"loading config as toml from: {self._config_file}")
                self._config = tomlkit.load(f)

    def apply_changes(self) -> None:
        """
        reload the config file itself
        :return:
        """
        with open(self._edited_fp, 'w') as f:
            tomlkit.dump(self._config, f)

    @LockedTracking.locked_access
    def get(self, *keys) -> Union[Dict, Any]:
        """
        get the config stack
        :return: get the stack
        """
        d = self._config
        for key in keys:
            d = d.get(key, None)
            if d is None:
                return None
        return d

    @LockedTracking.locked_access
    def set(self, value, *keys) -> None:
        """
        set a value in the config stack

        after that, the config file will be updated
        there will be a new file with the ending .edited
        that will be loaded instead of the original file
        to not overwrite the original file
        :return:
        """
        d = self._config
        for key in keys[:-1]:
            if key not in d:
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value

        self.apply_changes()
