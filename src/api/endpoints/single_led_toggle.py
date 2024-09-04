from flask_restful import reqparse, Resource
from flask import jsonify

from src.api.parent_resource_concepts import ApiEndpointManager
import logging as lg


class StateAccess(Resource):
    def get(self):
        lg.debug(self.thing._state)
        lg.debug(self.thing.state)
        return jsonify(self.thing._state)

    def post(self):
        p = reqparse.RequestParser()
        p.add_argument("state", required=True, location="args", type=bool)
        sargs = p.parse_args()

        self.thing.state = sargs.state
        return jsonify(self.thing.state)
