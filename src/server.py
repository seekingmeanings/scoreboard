#!/usr/bin/env python3

import logging as lg

# import redis

import tomlkit
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

# import re

# import environment stuff
from src.resources.single_led_toggle import StateAccess
from src.things.dummything import DummyVirtualThing

from src.board import BoardConfig


class BoardServer:
    def __init__(self, config_file: str):
        lg.debug("server instance init called")

        lg.info(f"loading config file: {config_file}")
        with open(config_file, "r") as f:
            self.config = tomlkit.load(f)

        # create working environment
        # self.thing = DummyVirtualThing()
        self.board = BoardConfig(
            chiffres_config_file=self.config["configs"]["chiffres"],
            board_config_file=self.config["configs"]["board_layout"]
        )

        # configure server
        self.app = Flask(self.config["server"]["name"])
        self.jtw = JWTManager(self.app)
        self.api = Api(self.app)

        lg.debug("adding resource points")
        self.api.add_resource(
            StateAccess, "/rest" + "/state", resource_class_kwargs={"thing": self.thing}
        )

    def run(self):
        lg.info("starting server")
        self.app.run(host="localhost", port=6969)


def main():
    lg.basicConfig(level="DEBUG")

    lg.debug(f"starting instance")

    server_instance = BoardServer(
        config_file="config.toml",
    )
    server_instance.run()
