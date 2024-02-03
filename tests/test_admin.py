import re

import pytest
from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User

from data_browser import orm_admin
from data_browser.admin import ViewAdmin
from data_browser.models import View


@pytest.fixture
def other_user():
    return User.objects.create(
        username="other", is_active=True, is_superuser=True, is_staff=True
    )


def make_view(**kwargs):
    View.objects.create(
        model_name="core.Product", fields="admin", query="name__contains=sql", **kwargs
    )


@pytest.fixture
def multiple_views(admin_user, other_user):
    make_view(owner=admin_user, name="my_in_folder", folder="my folder")
    make_view(owner=admin_user, name="my_out_of_folder")
    make_view(owner=other_user, name="other_in_folder", folder="other folder")
    make_view(owner=other_user, name="other_out_of_folder")


@pytest.fixture
def view(admin_user):
    return View(
        model_name="core.Product",
        fields="name+0,size-1,size_unit",
        query="name__equals=fred",
        owner=admin_user,
    )


def test_ddb_performance(admin_client, snapshot, multiple_views, mocker):
    View.objects.update(shared=True, public=True)

    get_models = mocker.patch(
        "data_browser.orm_admin.get_models", wraps=orm_admin.get_models
    )

    res = admin_client.get(
        "/data_browser/query/data_browser.View/"
        "name,valid,public_link,google_sheets_formula.json"
    )
    assert res.status_code == 200
    assert len(get_models.mock_calls) == 5


def test_open_view(view, rf):
    expected = (
        '<a href="/data_browser/query/core.Product/name+0,size-1,size_unit.html'
        '?name__equals=fred&limit=1000">view</a>'
    )
    assert ViewAdmin.open_view(view) == expected


def test_cant_add(admin_client):
    res = admin_client.get("/admin/data_browser/view/add/")
    assert res.status_code == 403


def test_public_links(view, admin_client):
    view.public = True
    view.save()
    res = admin_client.get(
        f"http://testserver/admin/data_browser/view/{view.pk}/change/"
    )
    assert res.status_code == 200
    expected = f"http://testserver/data_browser/view/{view.public_slug}.csv"
    assert expected in res.content.decode()

    view.fields = "bobit"
    view.save()
    res = admin_client.get(
        f"http://testserver/admin/data_browser/view/{view.pk}/change/"
    )
    assert res.status_code == 200

    expected = "View is invalid"
    assert expected in res.content.decode()


def test_is_valid(view, admin_user, admin_client):
    view.model_name = "data_browser.View"
    view.fields = "id"
    view.query = ""

    # no owner, not valid
    view.owner = None
    view.save()
    res = admin_client.get(
        f"http://testserver/admin/data_browser/view/{view.pk}/change/"
    )
    assert res.status_code == 200
    expected = (
        r'<label>Valid:</label>\s*<div class="readonly"><img'
        r' src="/static/admin/img/icon-no.svg" alt="False"></div>'
    )
    assert re.search(expected, res.content.decode())

    # all good, valid
    view.owner = admin_user
    view.save()
    res = admin_client.get(
        f"http://testserver/admin/data_browser/view/{view.pk}/change/"
    )
    assert res.status_code == 200
    expected = (
        r'<label>Valid:</label>\s*<div class="readonly"><img'
        r' src="/static/admin/img/icon-yes.svg" alt="True"></div>'
    )
    assert re.search(expected, res.content.decode())

    # invalid
    view.fields = "invalid"
    view.save()
    res = admin_client.get(
        f"http://testserver/admin/data_browser/view/{view.pk}/change/"
    )
    assert res.status_code == 200
    expected = (
        r'<label>Valid:</label>\s*<div class="readonly"><img'
        r' src="/static/admin/img/icon-no.svg" alt="False"></div>'
    )
    assert re.search(expected, res.content.decode())


@pytest.fixture
def get_admin_details(rf):
    def helper(admin_user, obj):
        request = rf.get("/")
        request.user = admin_user
        view_admin = ViewAdmin(View, admin.site)
        fields = set(flatten_fieldsets(view_admin.get_fieldsets(request, obj)))
        return fields

    return helper


@pytest.fixture
def staff_user(admin_user):
    admin_user.is_superuser = False
    admin_user.user_permissions.add(Permission.objects.get(codename="change_view"))
    return admin_user


class TestAdminFieldsSuperUser:
    def test_private_view_see_everything(self, admin_user, get_admin_details, view):
        fields = get_admin_details(admin_user, view)
        assert fields == {
            "description",
            "fields",
            "model_name",
            "name",
            "owner",
            "public",
            "public_slug",
            "query",
            "created_time",
            "google_sheets_formula",
            "id",
            "open_view",
            "public_link",
            "limit",
            "shared",
            "folder",
            "valid",
        }

    def test_public_view_see_everything(self, admin_user, get_admin_details, view):
        view.public = True
        fields = get_admin_details(admin_user, view)
        assert fields == {
            "description",
            "fields",
            "model_name",
            "name",
            "owner",
            "public",
            "public_slug",
            "query",
            "created_time",
            "google_sheets_formula",
            "id",
            "open_view",
            "public_link",
            "limit",
            "shared",
            "folder",
            "valid",
        }


class TestAdminFieldsStaffUser:
    def test_private_view_no_public_fields(self, staff_user, get_admin_details, view):
        fields = get_admin_details(staff_user, view)
        assert fields == {
            "description",
            "fields",
            "model_name",
            "name",
            "owner",
            "query",
            "created_time",
            "id",
            "open_view",
            "limit",
            "shared",
            "folder",
            "valid",
        }

    def test_public_view_readonly(self, staff_user, get_admin_details, view):
        view.public = True
        fields = get_admin_details(staff_user, view)
        assert fields == {
            "created_time",
            "description",
            "fields",
            "id",
            "model_name",
            "name",
            "open_view",
            "owner",
            "query",
            "limit",
            "shared",
            "folder",
            "valid",
        }
