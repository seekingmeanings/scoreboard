#!/usr/bin/env python3

from time import time

import argparse as ap
import logging as lg

# import redis
import secrets

import tomlkit
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

from dataclasses import dataclass

import json

# import re

# import environment stuff
from src.resources.single_led_toggle import StateAccess
from src.dummything import DummyVirtualThing

from src.board import BoardConfig


class BoardServer:
    def __init__(self, config_file: str):
        lg.debug("server instance init called")

        with open(config_file, "r") as f:
            self.config = tomlkit.load(f)

        # create working environment
        self.thing = DummyVirtualThing()
        self.board = BoardConfig(self.config["configs"]["board_layout"])

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
        # config=None,
    )
    server_instance.run()
