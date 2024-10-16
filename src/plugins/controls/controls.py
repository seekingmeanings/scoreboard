import logging
import os

from src.api.parent_resource_concepts import ApiEndpointManager
from src.helper.config import Config
from flask_restful import Resource, reqparse

from . import control_types


@ApiEndpointManager().add_resources(
    {'controls': 'controls'},
    "/controls/counter",
)
class GenericCounterAccess(Resource):
    """
    this is a super class to define the methods for counter
    accesses

    /rest/controls/counter?segmentgrp&operation

    :returns: 200
    """

    def post(self):
        p = reqparse.RequestParser()
        p.add_argument("segmentgrp", required=True, location="args", type=str)
        p.add_argument("operation", required=True, location="args", type=str)
        ps = p.parse_args()


class ControlsPlugin:
    """
    this is the init hook for the controls plugin

    it assembles the classes and Controls defined in the config file
    and adds them to the ControlManager ???? or via ApiManager???
    """

    def __init__(self, config_file, board, controls):
        self.lg = logging.getLogger(__name__)

        self.config = Config(str(os.path.join(os.path.dirname(__file__), config_file)))

        self.lg.debug("loading controls plugin instance")
        # init all the classes
        for control_conf_segment in self.config.get("segment_groups"):
            split_control_config_segment = self.config.get_sub_config(
                "segment_groups", control_conf_segment
            )
            segment_control_type = split_control_config_segment.get("type")

            self.lg.debug(f"--41{control_conf_segment}")
            if segment_control_type not in control_types.types:
                raise RuntimeError()

            # get the class
            controls.add_control(
                control_types.types[segment_control_type](
                    split_control_config_segment
                )
            )

