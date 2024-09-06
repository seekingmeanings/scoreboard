from dataclasses import dataclass
from typing import Dict
from src.things.activator import LED


@dataclass
class Digit:
    id: str = None
    type: str = None
    connections: Dict[str, LED] = None