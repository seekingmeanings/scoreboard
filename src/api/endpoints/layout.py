import flask_restful
from flask import jsonify

from src.api.parent_resource_concepts import ApiEndpointManager

import logging as lg


@ApiEndpointManager().add_resources(
    resources={"board": "board",
               "controls": "controls"},
    url="/board/layout"
)
class BoardLayoutAccess(flask_restful.Resource):
    def get(self):
        return jsonify({
            'segments': [
                {
                    'id': segment_id,
                    'digits': [
                        {'id': digit.id, 'type': digit.type}
                        for digit in segment

                    ],
                    'controls': [
                        {
                            'id': control.id,
                            'type': control.type,
                            'endpoint': control.api_call.joined_endpoint,
                            'method': control.api_call.method,
                        }
                        for control in self.controls.get_controls_by_segment(segment_id)
                    ]
                }
                for segment_id, segment in self.board.segments.items()
            ]

        }
        )
