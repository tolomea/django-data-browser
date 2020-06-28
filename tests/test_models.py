import pytest

from data_browser.models import View, global_data


@pytest.fixture
def view():
    return View(model_name="app.model", fields="+fa,-fd,fn", query="bob__equals=fred")


@pytest.fixture
def global_request(rf):
    request = rf.get("/")
    global_data.request = request
    yield request
    global_data.request = None


def test_str(view):
    view.name = "bob"
    assert str(view) == "app.model view: bob"


def test_public_link(view, global_request, settings):
    assert view.public_link() == "N/A"
    view.public = True
    expected = f"http://testserver/data_browser/view/{view.public_slug}.csv"
    assert view.public_link() == expected
    settings.DATA_BROWSER_ALLOW_PUBLIC = False
    assert view.public_link() == "Public Views are disabled in Django settings."


def test_google_sheets_formula(view, global_request, settings):
    assert view.google_sheets_formula() == "N/A"
    view.public = True
    expected = (
        f'=importdata("http://testserver/data_browser/view/{view.public_slug}.csv")'
    )
    assert view.google_sheets_formula() == expected
    settings.DATA_BROWSER_ALLOW_PUBLIC = False
    assert (
        view.google_sheets_formula() == "Public Views are disabled in Django settings."
    )
