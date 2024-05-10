from src.helper.race_condition import LockedTracking


class DummyVirtualThing(LockedTracking):
    def __init__(self) -> None:
        super().__init__()
        self._state = False

    @LockedTracking.locked_access
    @property
    def state(self):
        return self._state

    @LockedTracking.locked_access
    @state.setter
    def state(self, state: bool) -> bool:
        self._state = state
