from src.dummything import DummyVirtualThing
from flask_restful import reqparse
from flask import jsonify

from src.resources.parent_resource_concepts import ContentResource

class StateAccess(ContentResource):
    def get(self):
        return jsonify(self.thing.get_state())

    def post(self):
        p = reqparse.RequestParser()
        p.add_argument("state", required=True, location="args", type=bool)
        sargs = p.parse_args()

        self.thing.set_state(sargs.state)
        return self.get()
