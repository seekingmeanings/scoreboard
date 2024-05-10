#!/usr/bin/env python3

from time import time

import argparse as ap
import logging as lg

# import redis
import secrets
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

from dataclasses import dataclass

import json

# import re

from src.dummything import DummyVirtualThing


class ContentResource(Resource):
    def __init__(self, thing) -> None:
        super().__init__()
        self.thing = thing


class ConfigResource(Resource):
    pass


class StateAccess(ContentResource):
    def get(self):
        return jsonify(self.thing.get_state())

    def post(self):
        p = reqparse.RequestParser()
        p.add_argument("state", required=True, location="args", type=bool)
        sargs = p.parse_args()

        self.thing.set_state(sargs.state)
        return self.get()


class BoardServer:
    def __init__(self):
        lg.debug("server instance init called")

        # create working environment
        self.thing = DummyVirtualThing()

        # configure server
        self.app = Flask("SERVER NAME")
        self.jtw = JWTManager(self.app)
        self.api = Api(self.app)

        lg.debug("adding resource points")
        self.api.add_resource(
            StateAccess, "/rest" + "/state", resource_class_kwargs={"thing": self.thing}
        )

    def run(self):
        lg.info("starting server")
        self.app.run(host="localhost")


def main():
    lg.basicConfig(level="DEBUG")

    lg.debug(f"starting instance")

    server_instance = BoardServer(
        # config=None,
    )
    server_instance.run()


if __name__ == "__main__":
    main()
    lg.info("shutdown")
