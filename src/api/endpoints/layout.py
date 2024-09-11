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


@ApiEndpointManager().add_resources(
    resources={"board": "board"},
    url="/board/controls"
)
class BoardControlsAccess(flask_restful.Resource):
    def get(self):
        """
        get the control options for each segmentgroup
        :return:
        """
        # TODO: they have to be added somewhere in the plugin init \
        # either with a singelton manager or when the plugin is loaded
        # and a placeholder is passed on that the plugin can itself fill
        # with the controls
        return
