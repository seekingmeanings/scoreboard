from pprint import pprint as pp
import tomlkit as t

with open("../src/board_layout.toml") as f:
    stuff = t.load(f)

print()