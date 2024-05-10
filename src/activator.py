#!/usr/bin/env python3

class LED:
    def __init__(self, io_link, pin, name: str = None):
        self._state = False
        self.name = name
        self.pin = pin
        self.io_link = io_link

        self.io_link.pin_mode(
            self.pin,
            self.io_link.OUTPUT
        )

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
        self.io_link.digital_write(
            self.pin,
            self.io_link.HIGH if state else self.io_link.LOW
        )

    def toggle(self):
        self.state = False if self._state else True

    def on(self):
        self.state = True

    def off(self):
        self.state = False
