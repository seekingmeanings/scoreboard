from flask_restful import Resource, request
from flask import jsonify

from src.api.parent_resource_concepts import ApiEndpointManager

@ApiEndpointManager().add_resources(
    {'board': 'board'},
    "/ping"
)
class TestAccess(Resource):
    # TODO: add test for virtual
    @staticmethod
    def get():
        return jsonify("pong")
