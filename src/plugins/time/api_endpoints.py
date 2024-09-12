from src.api.parent_resource_concepts import ApiEndpointManager
from flask_restful import Resource
from flask import jsonify
from src.things.scoreboard.controls import Control


@ApiEndpointManager().add_resources(
    {'time': 'time'},
    "/plugins/time/active",
    [
        Control(
            segment="time",
            id="toggle",
            type="button",
            api_call=Control.ApiCall(
                method="POST",
                append_endpoint="/toggle"
            )
        ),
    ]
)
class TimeActiveAccess(Resource):
    def get(self):
        pass

    def post(self):
        pass
