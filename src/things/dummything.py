from src.helper.race_condition import LockedTracking


class DummyVirtualThing(LockedTracking):
    def __init__(self) -> None:
        super().__init__()
        self._state = False

    @LockedTracking.locked_access
    def _get_state(self):
        return self._state

    @LockedTracking.locked_access
    def _set_state(self, state: bool) -> bool:
        self._state = state

    state = property(fget=_get_state, fset=_set_state)