import pytest

from data_browser.common import global_state
from data_browser.common import set_global_state
from data_browser.models import View


@pytest.fixture
def view(admin_user):
    return View(
        model_name="core.Product",
        fields="name+0,size-1,size_unit",
        query="name__equals=fred",
        owner=admin_user,
    )


@pytest.fixture
def global_request(rf):
    request = rf.get("/")
    with set_global_state(request=request, public_view=False):
        yield global_state.request


def test_str(view):
    view.name = "bob"
    assert str(view) == "core.Product view: bob"


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
