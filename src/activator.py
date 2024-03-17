#!/usr/bin/env python3

class LED:
    def __init__(self, pin):
        self.state = False
        self.pin = pin

    def on(self):
        self.state = True
    
    def off(self):
        self.state = False