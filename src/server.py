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
            character_config_file=self.config["configs"]["characters"],
            board_config_file=self.config["configs"]["board_layout"],
            virtual=virtual
        )}

        # configure server
        self.app = Flask(self.config["server"]["name"])
        # self.jtw = JWTManager(self.app)
        self.api = Api(self.app)

        flask_cors.CORS(self.app)

        self.api_manager = ApiEndpointManager(self.api, self.resources)

        # load plugins
        self.external_plugins: list = list()
        self.load_plugins_from_conf(
            self.config['plugins']
        )

        lg.debug("adding internal api  endpoints")
        # TODO: link them dynamic with the help of config and themselves

        self.api.base_url = "/rest"

        # have to call that explicitly so the init is finished
        # TODO: make that from config
        self.api_manager.import_endpoint_module("src.api.endpoints")

    def load_plugin(self, plugin_mod, plugin_conf):
        # do the real plugin init and stuff
        print(plugin_mod)
        print(plugin_conf)

        # autostart

    def load_plugins_from_conf(self, plugin_conf_head: dir):
        # TODO: should they all be in the config, or can they be loaded by just the plugin dir???
        for plugin_name, plugin_conf in plugin_conf_head["p"].items():
            self.external_plugins.append(
                importlib.import_module(
                    name=f".{plugin_name}",
                    package=plugin_conf_head['dir']
                )
            )

            print(plugin_conf['active'])
            if 'active' in plugin_conf and plugin_conf['active'] is True:
                self.load_plugin(self.external_plugins[-1], plugin_conf)

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
