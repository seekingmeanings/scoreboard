from src.helper.race_condition import LockedTracking


class LED(LockedTracking):
    def __init__(self, io_link, pin, constants, name: str = None):
        super().__init__()

        self._state = False
        self.name = name
        self.constants = constants
        self.pin = getattr(self.constants, pin)
        self.io_link = io_link

        self.io_link.pin_mode(
            self.pin,
            self.constants.OUTPUT
        )

    # TODO: do i even want the locking on the lowest level? cause its gon fuck with overwrites in the end
    @property
    @LockedTracking.locked_access
    def state(self):
        return self._state

    @state.setter
    @LockedTracking.locked_access
    def state(self, state):
        self._state = state
        self.io_link.digital_write(
            self.pin,
            # inverted ???
            self.constants.LOW if state else self.constants.HIGH
        )

    def toggle(self):
        self.state = False if self._state else True

    def on(self):
        self.state = True

    def off(self):
        self.state = False
