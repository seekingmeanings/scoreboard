from pprint import pprint as pp
import tomlkit as t

with open("board_layout.toml") as f:
    stuff = t.load(f)

print()