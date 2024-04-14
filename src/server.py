#!/usr/bin/env python3

from time import time

import argparse as ap
import logging as lg

# import redis
import secrets
from flask import Flask, request, send_file
from flask_restful import Resource, Api, reqparse

from dataclasses import dataclass

import json
# import re

class ContentRessource(Resource, AccessCheck):
    pass

class ConfigRessource(Resource, AccessCheck):
    pass


class StateAccess(ContentRessource):
    
    def get(self):
        return




class BoardServer:
    def __init__(self):
        lg.debug("server instance init called")

        self.app = Flask("SERVER NAME")
        self.api = Api(self.app)

        lg.debug("adding resource points")


    def run(self):
        lg.info("starting server")
        self.app.run()







def main():

    lg.basicConfig(level="DEBUG")

    lg.dubg(f"starting instance")
    server_instance = BoardServer(
        config=None,
    )



if __name__ == "__main__":
    main()