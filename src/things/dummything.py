from src.helper.race_condition import LockedTracking


class DummyVirtualThing(LockedTracking):
    def __init__(self) -> None:
        super().__init__()
        self._state = False

    @LockedTracking.locked_access
    @property
    def state(self):
        return self._state

    @state.setter
    @LockedTracking.locked_access
    def state(self, state: bool) -> bool:
        self._state = state
