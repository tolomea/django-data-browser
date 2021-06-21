from textwrap import dedent, indent

from django.db.models import ExpressionWrapper, Field, Q

SPACES = "    "


def _format_value(value):
    if isinstance(value, Q):
        assert not value.negated
        assert value.connector == Q.AND

        children = ", ".join(f"{f}={_format_value(v)}" for f, v in value.children)
        return f"Q({children})"
    elif isinstance(value, Field):
        return f"{value.__class__.__name__}()"
    elif isinstance(value, ExpressionWrapper):
        expression = _format_value(value.expression)
        output_field = _format_value(value.output_field)
        return dedent(
            f"ExpressionWrapper(\n{indent(expression, SPACES)},\n{SPACES}output_field={output_field},\n)"
        )
    else:
        return repr(value)


class DebugQS:
    def __init__(self, s):
        self.s = s

    def __getattr__(self, name):
        return DebugQS(f"{self.s}.{name}")

    def __call__(self, *args, **kwargs):
        if args or kwargs:
            flat_args = ",\n".join(
                [_format_value(a) for a in args]
                + [f"{n}={_format_value(v)}" for n, v in kwargs.items()]
            )
            return DebugQS(f"{self.s}(\n{indent(flat_args, SPACES)},\n)")
        else:
            return DebugQS(f"{self.s}()")

    def __getitem__(self, index):
        if isinstance(index, slice):
            assert index.start is None
            assert index.step is None
            return DebugQS(f"{self.s}[: {index.stop}]")
        else:  # pragma: no cover
            return DebugQS(f"{self.s}[index]")

    def __str__(self):
        return self.s

    def __repr__(self):
        return self.s
