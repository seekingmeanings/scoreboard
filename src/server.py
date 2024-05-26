#!/usr/bin/env python3

import logging as lg

import importlib

import tomlkit
from flask import Flask
from flask_restful import Api
# from flask_jwt_extended import JWTManager

# import environment stuff
from src.resources.digit import DisplayDigitAccess, BoardAccess, LEDAccess
from src.resources.test import TestAccess

from src.scoreboard import Scoreboard


class BoardServer:
    def __init__(self, config_file: str, virtual: bool = False):
        lg.debug("server instance init called")

        lg.info(f"loading config file: {config_file}")
        with open(config_file, "r") as f:
            self.config = tomlkit.load(f)

        # create working environment
        # self.thing = DummyVirtualThing()
        self.board = Scoreboard(
            chiffres_config_file=self.config["configs"]["chiffres"],
            board_config_file=self.config["configs"]["board_layout"],
            virtual=virtual
        )

        # configure server
        self.app = Flask(self.config["server"]["name"])
        # self.jtw = JWTManager(self.app)
        self.api = Api(self.app)

        # load plugins
        self.external_plugins: list = list()
        # TODO: self.load_plugins()

        lg.debug("adding resource points")
        # TODO: link them dynamic with the help of config and themselves
        self.api.add_resource(
            DisplayDigitAccess, "/rest" + "/display",
            resource_class_kwargs={
                "board": self.board
            }
        )
        self.api.add_resource(
            BoardAccess,
            "/rest" + "/board-state",
            resource_class_kwargs={
                "board": self.board
            }
        )
        self.api.add_resource(
            LEDAccess,
            "/rest" + "/led",
            resource_class_kwargs={
                "board": self.board
            }
        )
        self.api.add_resource(
            TestAccess,
            "/rest" + "/ping"
        )

    def _load_plugins(self, plugin_mod, plugin_conf):
        # do the real plugin init and stuff
        pass

    def load_plugins(self, plugin_dir=None, plugin_conf: dir = None):
        if plugin_dir:
            self.external_plugins.append(importlib.import_module(plugin_dir))
            self._load_plugins(self.external_plugins[-1], plugin_conf)

        for plugin_name, plugin_conf in self.config["plugins"].items():
            if not plugin_conf["active"]:
                continue
            # load plugin
            raise NotImplementedError()

    def run(self):
        lg.info("starting server")
        self.app.run(host="localhost", port=6969)


def main(args):
    lg.basicConfig(level="DEBUG")

    lg.debug(f"starting instance")

    server_instance = BoardServer(
        config_file="config.toml",
        virtual=args.virtual
    )
    server_instance.run()
