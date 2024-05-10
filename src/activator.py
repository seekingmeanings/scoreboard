#!/usr/bin/env python3

class LED:
    def __init__(self, io_link, pin, constants, name: str = None):
        self._state = False
        self.name = name
        self.constants = constants
        self.pin = getattr(self.constants, pin)
        self.io_link = io_link

        print(self.pin)

        self.io_link.pin_mode(
            self.pin,
            self.constants.OUTPUT
        )

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
        self.io_link.digital_write(
            self.pin,
            self.constants.HIGH if state else self.constants.LOW
        )

    def toggle(self):
        self.state = False if self._state else True

    def on(self):
        self.state = True

    def off(self):
        self.state = False
