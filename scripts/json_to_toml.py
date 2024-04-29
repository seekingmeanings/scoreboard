#!/usr/bin/env python3


# concept from:
# https://gist.github.com/pgilad/e8ffd8ce2bde81a1a375e86df77a34ab

import json
import sys
import tomlkit

try:
    json_file = str(sys.argv[1])
    output_file = str(sys.argv[2])

    with (open(json_file) as source, open(output_file, "w") as target):
        target.write(tomlkit.dumps(json.loads(source.read())))
except (TypeError, IndexError):
    raise Exception("json_to_toml.py input.json output.toml")