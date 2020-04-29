import json
from collections import defaultdict

import pytest
from data_browser.models import View
from data_browser.query import ASC, DSC, Query


@pytest.fixture
def query():
    return Query(
        "app.model", {"fa": ASC, "fd": DSC, "fn": None}, [("bob", "equals", "fred")]
    )


@pytest.fixture
def view(query):
    filters = defaultdict(list)
    for k, v in query.filter_fields:
        filters[k].append(v)

    return View(
        model=query.model_name, fields=query.field_str, query=json.dumps(filters)
    )


def test_round_trip_save(query, view):
    assert view.get_query("html") == query


def test_str(view):
    view.name = "bob"
    assert str(view) == "app.model view: bob"
