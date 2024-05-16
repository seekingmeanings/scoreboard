from src.resources.parent_resource_concepts import ContentResource
from flask_restful import reqparse, request
from flask import jsonify
import logging as lg


class DisplayDigitAccess(ContentResource):
    def post(self):
        p = reqparse.RequestParser()
        p.add_argument("digit", location="args", type=str)
        p.add_argument("content", location="args", type=str)
        sargs = p.parse_args()
        lg.debug(f"setting display {sargs.digit} to {sargs.content}")

        try:
            self.board.display_char(sargs.digit, sargs.content)
        except OverflowError:
            return "invalid op", 500


class BoardAccess(ContentResource):
    def get(self):
        return jsonify(self.board.get_board_state())
