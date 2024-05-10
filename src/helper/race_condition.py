from time import gmtime
from threading import RLock
from functools import wraps


class LockedTracking:
    def __init__(self) -> None:
        self._last_access = None
        self._lock = RLock()

    @staticmethod
    def locked_access(_func=None, *, track=True):
        def exec_wrap(func):
            @wraps
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
