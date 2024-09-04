#!/usr/bin/env python3

import logging as lg

import importlib

import flask_cors
import tomlkit
from flask import Flask
from flask_restful import Api
# from flask_jwt_extended import JWTManager

# import environment stuff
from src.api.parent_resource_concepts import ApiEndpointManager

from src.things.scoreboard.scoreboard import Scoreboard


class BoardServer:
    def __init__(self, config_file: str, virtual: bool = False):
        lg.debug("server instance init called")

        lg.info(f"loading config file: {config_file}")
        with open(config_file, "r") as f:
            self.config = tomlkit.load(f)

        # create working environment
        # self.thing = DummyVirtualThing()

        self.resources = {"board": Scoreboard(
            chiffres_config_file=self.config["configs"]["chiffres"],
            board_config_file=self.config["configs"]["board_layout"],
            virtual=virtual
        )}

        # configure server
        self.app = Flask(self.config["server"]["name"])
        # self.jtw = JWTManager(self.app)
        self.api = Api(self.app)

        flask_cors.CORS(self.app)

        # load plugins
        self.external_plugins: list = list()
        # TODO: self.load_plugins()

        lg.debug("adding resource points")
        # TODO: link them dynamic with the help of config and themselves

        self.api.base_url = "/rest"
        tmpurl = "/rest"

        # have to call that explicitly so the init is finished
        self.api_manager = ApiEndpointManager(self.api, self.resources)
        self.api_manager.import_endpoint_module("src.api.endpoints")

        print("old method")
        self.api_manager.auto_add_endpoints()


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


i_dont_wanna_use_globals_but_fuck_idk_how = None
