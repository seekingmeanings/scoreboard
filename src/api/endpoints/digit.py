from src.api.parent_resource_concepts import (
    ApiEndpointManager,

    PopulateApiResource, register_api_endpoint,
    add_resource
)
from flask_restful import reqparse, request, Resource
from flask import jsonify
import logging as lg

"""
OMGOMG

DONT IMPORT FROM THE PARENT RES CONCEPTS
BUT IMPORT THE INSTANCE OF THE SERVER•PY FILESEEEEE

"""


class DisplayDigitAccess(PopulateApiResource):
    def post(self):
        p = reqparse.RequestParser()
        p.add_argument("digit", required=True, location="args", type=str)
        p.add_argument("content", location="args", type=str)
        sargs = p.parse_args()
        lg.debug(f"setting display {sargs.digit} to {sargs.content}")

        try:
            self.board.display_char(sargs.digit, sargs.content)
        except OverflowError:
            return "invalid op", 500


@ApiEndpointManager().add_resources(
    {'board': 'board'},
    "/board"
)
class BoardAccess(Resource):
    def get(self):
        return jsonify(self.board.get_board_state())


@ApiEndpointManager().add_resources(
    {'board': 'board'},
    "/led"
)
class LEDAccess(PopulateApiResource):
    def get(self):
        p = reqparse.RequestParser()
        p.add_argument("digit", required=True, location="args", type=str)
        p.add_argument("led_id", location="args", type=str, required=True)
        args = p.parse_args()

        return self.board.digits[args.digit][args.led_id].state

    def post(self):
        p = reqparse.RequestParser()
        p.add_argument("digit", required=True, location="args", type=str)
        p.add_argument("led_id", location="args", type=str, required=True)
        p.add_argument("state", required=True, location="args", type=bool)
        args = p.parse_args()

        self.board.digits[args.digit][args.led_id].state = bool(args.state)
