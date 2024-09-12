#!/usr/bin/env python3
import concurrent.futures
import threading

import logging

import importlib

import flask_cors
import tomlkit
from flask import Flask
from flask_restful import Api
# from flask_jwt_extended import JWTManager

# import environment stuff
from src.api.parent_resource_concepts import ApiEndpointManager

from src.things.scoreboard.scoreboard import Scoreboard
from src.things.scoreboard.controls import ControlManager

from typing import List, Dict


class BoardServer:
    def __init__(self, config_file: str, virtual: bool = False):
        self.lg = logging.getLogger(self.__class__.__name__)
        self.lg.debug("server instance init called")

        self.lg.info(f"loading config file: {config_file}")
        with open(config_file, "r") as f:
            self.config = tomlkit.load(f)

        # create working environment
        # self.thing = DummyVirtualThing()

        self.resources = {"board": Scoreboard(
            character_config_file=self.config["configs"]["characters"],
            board_config_file=self.config["configs"]["board_layout"],
            virtual=virtual),
            "config": self.config,
            'controls': ControlManager()
        }
        self.lg.debug(self.resources)

        # configure server
        self.app = Flask(self.config["server"]["name"])
        # self.jtw = JWTManager(self.app)
        self.api = Api(self.app)
        self.api.base_url = self.config["api"]["base_url"]

        flask_cors.CORS(self.app)

        self.api_manager = ApiEndpointManager(self.api, self.resources, self.resources['controls'])

        # load plugins
        self.threads: List = []
        self.external_plugins_modules: List = list()
        self.external_plugins: List = list()
        self.get_plugins_from_conf(
            self.config['plugins']
        )

        self.lg.debug("adding internal api  endpoints")
        # TODO: link them dynamic with the help of config and themselves

        self.api.base_url = "/rest"

        # have to call that explicitly so the init is finished
        # TODO: make that from config
        self.api_manager.import_endpoint_module("src.api.endpoints")


        # start the threads
        self.start_threads()

    def start_threads(self):
        for thread in self.threads:
            thread.start()

    def load_plugin(self, plugin_hook, plugin_conf):
        # do the real plugin init and stuff
        self.lg.debug(f"loading plugin {plugin_hook}")
        plugin = plugin_hook(
            **plugin_conf['init']['args'],
            **{
                arg_name:
                self.resources[arg_name]
                for arg_name in plugin_conf['init']['resources']
            }
        )
        self.external_plugins.append(plugin)

        # autostart
        if plugin_conf['autostart']:
            self.lg.debug(f"preparing autostart plugin: {plugin}")
            self.threads.append(threading.Thread(target=plugin.run, daemon=True))

        self.lg.debug(f"finished loading plugin {plugin}")

    def get_plugins_from_conf(self, plugin_conf_head: dir):
        # TODO: should they all be in the config, or can they be loaded by just the plugin dir???
        for plugin_name, plugin_conf in plugin_conf_head["p"].items():
            self.external_plugins_modules.append(
                importlib.import_module(
                    name=f".{plugin_name}",
                    package=plugin_conf_head['dir']
                )
            )

            if 'active' in plugin_conf and plugin_conf['active'] is True:
                # TODO: make sure the plugins are not loading at the same time
                self.load_plugin(self.external_plugins_modules[-1].init_hook, plugin_conf)

            self.api_manager.import_endpoint_module(
                self.external_plugins_modules[-1].__name__
            )

    def run(self):
        self.lg.info("starting server")
        self.app.run(host="localhost", port=6969)


def main(args):
    logging.basicConfig(level=args.verbosity)
    logger = logging.getLogger(__name__)
    logger.info(f"starting instance")

    server_instance = BoardServer(
        config_file="config.toml",
        virtual=args.virtual
    )
    logger.info(f"server instance created")
    
    server_instance.run()
