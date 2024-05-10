from time import gmtime
from threading import RLock

from src.helper.race_condition import LockedTracking

class DummyVirtualThing:
    def __init__(self) -> None:
        self._state = False
        self.last_access = None
        self._lock = RLock()

    def _locked_access(_func=None, *, track=True):
        if _func:
            exit(6666)
        def exec_wrap(func):
            def wrapper(*args, **kwargs):
                wrapped_self = args[0]
                with wrapped_self._lock:
                    if track:
                        wrapped_self.last_access = gmtime()
                    return func(*args, **kwargs)
            return wrapper
        if _func is None:
            return exec_wrap
        else:
            return exec_wrap(_func)

    @_locked_access(track=False)
    def last_access(self):
        return self.last_access

    @LockedTracking.locked_access
    def set_state(self, state: bool):
        self._state = state

    @_locked_access
    def get_state(self) -> bool:
        return self._state
