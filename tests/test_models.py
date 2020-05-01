import pytest
from data_browser.models import View


@pytest.fixture
def view():
    return View(model_name="app.model", fields="+fa,-fd,fn", query="bob__equals=fred")


def test_str(view):
    view.name = "bob"
    assert str(view) == "app.model view: bob"
