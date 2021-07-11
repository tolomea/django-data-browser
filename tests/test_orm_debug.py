import pytest
from django.db.models import Q

from data_browser.orm_debug import _format_value


@pytest.mark.parametrize(
    "value,expected",
    [
        (Q("bob"), "Q('bob')"),
        (Q(bob="fred"), "Q(bob='fred')"),
        (Q("tom", bob="fred"), "Q('tom', bob='fred')"),
        (Q("bob") & Q("fred"), "Q('bob', 'fred')"),
        (Q("bob") | Q("fred"), "Q('bob') | Q('fred')"),
        (~(Q("bob") & Q("fred")), "~Q('bob', 'fred')"),
        (~(Q("bob") | Q("fred")), "~Q(Q('bob') | Q('fred'))"),
        (~Q(bob=None), "~Q(bob=None)"),
        (~Q(~Q("bob")), "~Q(~Q('bob'))"),
    ],
)
def test_format_value(value, expected):
    assert _format_value(value) == expected
