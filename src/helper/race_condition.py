from time import gmtime
from threading import RLock

class LockedTracking:
    def __init__(self) -> None:
        self._last_access = None
        self._lock = RLock()

    # TODO: is this supposed to be static?
    @staticmethod
    def locked_access(_func=None, *, track=True):
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