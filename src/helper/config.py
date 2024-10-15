from src.helper.race_condition import LockedTracking
from typing import Any, List, Dict, Union
import os
import tomlkit
import logging


class Config(LockedTracking):
    def __init__(self, config_file: str = None,
                 config_data=None,
                 parent=None,
                 parent_keys=None) -> None:
        # TODO get __file__ for init to get the global filepath here instead of the other class
        super().__init__()

        # TODO: sub config has extra logger
        self.lg = logging.getLogger(__name__)

        if config_file:
            self.edited_affix = ".edited"
            self._config_file = config_file
            self._edited_fp = self._config_file + self.edited_affix

            # load the config file
            self._config = self._load_config()

        else:
            self._config = config_data
            self.config_file = None

        self.parent = parent
        self.parent_keys = parent_keys or []

    def _load_config(self) -> Dict:
        """
        load the config file

        if an edited version exists, load it instead
        :return:
        """
        if os.path.exists(self._edited_fp):
            with open(self._edited_fp, "r") as f:
                self.lg.info(f"loading config as toml from: {self._edited_fp}")
                return tomlkit.load(f)

        with open(self._config_file, "r") as f:
            self.lg.info(f"loading config as toml from: {self._config_file}")
            return tomlkit.load(f)

    def apply_changes(self) -> None:
        """
        reload the config file itself
        :return:
        """
        if self.parent:
            self.parent.set(self._config, *self.parent_keys)

        elif self.config_file:
            with open(self._edited_fp, 'w') as f:
                tomlkit.dump(self._config, f)
        else:
            self.lg.warning("something went wrong, no parent and not a parent itself")

    @LockedTracking.locked_access
    def get(self, *keys) -> Union[Dict, Any]:
        """
        get the config stack
        :return: get the stack
        """
        # TODO: _config is only when loaded file???
        # TODO: need to make sure where data is in subclasses
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

    def get_sub_config(self, *keys):
        subset = self.get(*keys)
        if subset is None:
            subset = {}
            self.set(subset, *keys)

        return Config(config_data=subset, parent=self, parent_keys=keys)
