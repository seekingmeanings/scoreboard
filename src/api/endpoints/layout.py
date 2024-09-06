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
        return jsonify({
            'segments': [
                {
                    'id': segment_id,
                    'digits': [
                        {'id': digit.id, 'type': digit.type}
                        for digit in segment

                    ]
                }
                for segment_id, segment in self.board.segments.items()
            ]

        }
        )
