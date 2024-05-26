import tomllib


class ConfigLoader:
    def __init__(self, config_file: str) -> None:
        self.config: dict = dict()
        self.config_file: str = config_file
        self.load_toml_config(self.config_file)

    def load_toml_config(self, config_file) -> None:
        with open(
                self.config_file if self.config_file else config_file, 'rb'
        ) as f:
            self.config = tomllib.load(f)
