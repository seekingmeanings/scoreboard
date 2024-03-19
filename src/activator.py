#!/usr/bin/env python3

class ExdenderBoard:
    def __init__(self, address) -> None:
        self.address = address
        self.leds = []

    def add_led(self, pin) -> 'LED':
        led = LED(pin)
        self.leds.append(led)
        return led

class LED:
    def __init__(self, pin) -> None:
        self.state = False
        self.pin = pin

    def on(self) -> None:
        self.state = True
    
    def off(self) -> None:
        self.state = False