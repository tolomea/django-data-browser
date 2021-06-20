class DebugQS:
    def __init__(self, s):
        self.s = s

    def __getattr__(self, name):
        return DebugQS(f"{self.s}.{name}")

    def __call__(self, *args, **kwargs):
        if args or kwargs:
            flat_args = ", ".join(
                [repr(a) for a in args] + [f"{n}={v!r}" for n, v in kwargs.items()]
            )
            return DebugQS(f"{self.s}(\n    {flat_args}\n)")
        else:
            return DebugQS(f"{self.s}()")

    def __getitem__(self, slice):
        assert slice.start is None
        assert slice.step is None
        return DebugQS(f"{self.s}[: {slice.stop}]")

    def __str__(self):
        return self.s
