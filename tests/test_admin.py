import pytest
from data_browser.admin import ViewAdmin, globals
from data_browser.models import View
from django.contrib import admin
from django.contrib.auth.models import Permission, User


@pytest.fixture
def view(admin_user):
    return View(model_name="app.model", fields="fa+0,fd-1,fn", query="bob__equals=fred")


def test_open_view(view, rf):
    expected = '<a href="/data_browser/query/app.model/fa+0,fd-1,fn.html?bob__equals=fred">view</a>'
    assert ViewAdmin.open_view(view) == expected


def test_public_link(view, rf):
    globals.request = rf.get("/")
    assert ViewAdmin.public_link(view) == "N/A"
    view.public = True
    expected = f"http://testserver/data_browser/view/{view.pk}.csv"
    assert ViewAdmin.public_link(view) == expected
    globals.request = None


def test_google_sheets_formula(view, rf):
    globals.request = rf.get("/")
    assert ViewAdmin.google_sheets_formula(view) == "N/A"
    view.public = True
    expected = f'=importdata("http://testserver/data_browser/view/{view.pk}.csv")'
    assert ViewAdmin.google_sheets_formula(view) == expected
    globals.request = None


def test_add_has_user(admin_client):
    user = User.objects.get()
    res = admin_client.get("/admin/data_browser/view/add/")
    assert res.status_code == 200
    assert res.context[0]["adminform"].form.initial["owner"] == user.pk


def test_change_form_links_have_full_url(view, admin_client):
    view.public = True
    view.save()
    res = admin_client.get(
        f"http://testserver/admin/data_browser/view/{view.pk}/change/"
    )
    assert res.status_code == 200

    all_fields = [f for fs in res.context[0]["adminform"] for l in fs for f in l]
    for field in all_fields:
        if field.is_readonly and field.field["name"] == "public_link":
            expected = f"http://testserver/data_browser/view/{view.pk}.csv"
            assert field.contents() == expected
            break
    else:
        assert False


def test_readonly_fields(view, rf, admin_user):
    request = rf.get("/")
    request.user = admin_user
    view_admin = ViewAdmin(View, admin.site)

    # no object, add page, everything editable
    assert view_admin.get_readonly_fields(request, None) == [
        "open_view",
        "public_link",
        "google_sheets_formula",
        "id",
        "created_time",
    ]

    # user has public perms can do anything
    assert view_admin.get_readonly_fields(request, view) == [
        "open_view",
        "public_link",
        "google_sheets_formula",
        "id",
        "created_time",
    ]

    # user has public perms can do anything even to a public view
    view.public = True
    assert view_admin.get_readonly_fields(request, view) == [
        "open_view",
        "public_link",
        "google_sheets_formula",
        "id",
        "created_time",
    ]
    view.public = False

    # user doesn't have public perms, can't edit public flag
    admin_user.is_superuser = False
    admin_user.user_permissions.add(Permission.objects.get(codename=f"change_view"))
    assert view_admin.get_readonly_fields(request, view) == [
        "open_view",
        "public_link",
        "google_sheets_formula",
        "id",
        "created_time",
        "public",
    ]

    # user doesn't have public perms, view is public, can't do anything
    view.public = True
    assert view_admin.get_readonly_fields(request, view) == [
        "name",
        "owner",
        "public",
        "open_view",
        "public_link",
        "google_sheets_formula",
        "description",
        "model_name",
        "fields",
        "query",
        "id",
        "created_time",
    ]
