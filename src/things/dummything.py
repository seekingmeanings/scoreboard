from src.helper.race_condition import LockedTracking


class DummyVirtualThing(LockedTracking):
    def __init__(self) -> None:
        super().__init__()
        self._state = False

        raise RuntimeWarning("use with caution, state is bugged, cause of some decorator bs")

    @property
    @LockedTracking.locked_access()
    def state(self):
        return self._state

    @LockedTracking.locked_access()
    @state.setter
    def state(self, state: bool) -> bool:
        self._state = state

    #state = property(fget=_get_state, fset=_set_state)