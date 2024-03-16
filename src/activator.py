#!/usr/bin/env python3

class LED:
    def __init__(self, color):
        self.color = color
        self.state = False

    def toggle(self):
        self.state = not self.state
        print(f'Toggling {self.color} LED: {self.state}')