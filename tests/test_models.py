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


@pytest.fixture
def view(query):
    return View(**query.save_params)


def test_round_trip_save(query, view):
    assert view.get_query("html") == query


def test_str(view):
    view.name = "bob"
    assert str(view) == "model view: bob"
