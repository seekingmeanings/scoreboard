from dataclasses import dataclass
from typing import Dict, List, AnyStr, LiteralString
import logging

@dataclass
class Control:
    """
    following control types are available:
    - button
        single button that does a simple call
    """

    @dataclass
    class ApiCall:
        method: str = 'POST'
        joined_endpoint: str = None
        append_endpoint: str = None
        # TODO: implement parsing meth
        data: Dict = None

        def make_call(self, endpoint: str):
            logging.warning(f"MAKE CALLLLLLLLLLLLLLLL for {endpoint}")
            self.joined_endpoint = endpoint.join(self.append_endpoint) if self.append_endpoint else endpoint
            logging.warning(self.joined_endpoint)

    segment: AnyStr = None
    id: AnyStr = None
    type: AnyStr = None
    api_call: ApiCall = None



class ControlManager:
    def __init__(self):
        self._controls: List[Control] = []

    def add_control(self, control: Control):
        if control in self._controls:
            raise ValueError("Control already exists")
        self._controls.append(control)

    def get_controls_by_segment(self, segment_id: str) -> List[Control]:
        return [control for control in self._controls if control.segment == segment_id]
