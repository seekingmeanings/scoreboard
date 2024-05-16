from src.resources.parent_resource_concepts import ContentResource
from flask_restful import reqparse
from flask import jsonify
import logging as lg

class DisplayDigitAccess(ContentResource):
    def post(self):
        p = reqparse.RequestParser()
        p.add_argument("digit", location="args", type=str)
        p.add_argument("content", location="args")
        args = p.parse_args()

        lg.debug(f"setting display {args.digit} to {args.content}")

        try:
            self.board.display_char(args.id, args.content)
        except OverflowError:
            return "invalid op", 500

