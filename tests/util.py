class ANY:  # pragma: no cover
    def __init__(self, type):
        self.type = type

    def __eq__(self, other):
        return isinstance(other, self.type)


class KEYS:  # pragma: no cover
    def __init__(self, *keys):
        self.keys = set(keys)

    def __eq__(self, other):
        return isinstance(other, dict) and other.keys() == self.keys
