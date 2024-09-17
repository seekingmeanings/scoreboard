from src.api.parent_resource_concepts import ApiEndpointManager
from flask_restful import Resource, reqparse, inputs
from flask import jsonify
from src.things.scoreboard.controls import Control
from typing import LiteralString


@ApiEndpointManager().add_resources(
    {'time': 'time'},
    "/plugins/time/active",
    [
        Control(
            segment="time",
            id="toggle",
            label="toggle",
            type="button",
            api_call=Control.ApiCall(
                method="POST",
                # append_endpoint="/toggle",
            )
        ),
    ]
)
class TimeActiveAccess(Resource):
    def get(self):
        return jsonify(self.time.display_time)

    def post(self):
        p = reqparse.RequestParser()
        p.add_argument("state", required=False, location="args", type=inputs.boolean)
        ps = p.parse_args()
        try:
            if ps.state is None:
                self.time.display_time_toggle()
            else:
                self.time.display_time = ps.state
            return self.time.display_time
        except RuntimeError:
            return jsonify("time plugin not running"), 409
