import json
from pathlib import Path


class ANY:
    def __init__(self, type):
        self.type = type

    def __eq__(self, other):
        return isinstance(other, self.type)


class KEYS:
    def __init__(self, *keys):
        self.keys = set(keys)

    def __eq__(self, other):
        return isinstance(other, dict) and other.keys() == self.keys


def update_fe_fixture(filename, data):  # pragma: no cover
    filename = Path(filename)

    if filename.exists():
        with filename.open("r") as f:
            current = json.load(f)
    else:
        current = None

    if data != current:
        with filename.open("w") as f:
            json.dump(data, f, indent=4, sort_keys=True)
            f.write("\n")
