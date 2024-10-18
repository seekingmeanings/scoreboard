import logging
from src.helper.config import Config
from typing import Callable


class Operation:
    @staticmethod
    def increment(val: int, step: int = 1) -> int:
        return val + step

    @staticmethod
    def decrement(val: int, step: int = 1) -> int:
        return val - 1


class Counter:
    def __init__(self, config: Config, board_maybe_idk):
        self.lg = logging.getLogger(__name__)
        self.config = config
        self.lg.error(self.config)

        # stuff
        #   overflow
        #   max, min, step
        #   reset, just prevent if false

        self._steps = {
            i: val
            for i, val in enumerate(range(
                self.config.get(["min"]),
                self.config.get(["max"]),
                self.config.get(["step"]),
            ))
        }

        self._index = 0

        self._count: int = self.config.get(["start_value"]) if \
            self.config.get(["start_value"]) else self._steps[0]

    @property
    def count(self) -> int:
        # TODO: how do i interface the count?
        # TODO: board segments would make most sense right
        return self._count

    @count.setter
    def count(self, new_value: int) -> None:
        self.lg.error(f"setting to {new_value}")
        raise NotImplementedError

    def op(self, operation: Callable[[Operation, int], int]):
        n_idx = operation(self._index)
        if n_idx not in self._steps:
            raise IndexError

        self.count = n_idx

    def reset(self):
        if self.config.get(["reset"]):
            self.count = 0


types = {
    "counter": Counter,
}
