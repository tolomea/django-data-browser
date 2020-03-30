import pytest
from data_browser.models import View
from data_browser.query import ASC, DSC, Query


@pytest.fixture
def query():
    return Query(
        "app",
        "model",
        {"fa": ASC, "fd": DSC, "fn": None},
        "html",
        [("bob", "equals", "fred")],
    )


def test_round_trip_save(query):
    obj = View(**query.save_params)
    assert obj.get_query("html") == query
