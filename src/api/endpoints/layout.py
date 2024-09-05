import flask_restful
from flask import jsonify

from src.api.parent_resource_concepts import ApiEndpointManager

import logging as lg

@ApiEndpointManager().add_resources(
    resources={"board": "board"},
    url="/board/layout"
)
class BoardLayoutAccess(flask_restful.Resource):
    def get(self):
        return