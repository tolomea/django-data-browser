import pytest
from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.auth.models import Permission, User

from data_browser.admin import ViewAdmin
from data_browser.models import View


@pytest.fixture
def view(admin_user):
    return View(model_name="app.model", fields="fa+0,fd-1,fn", query="bob__equals=fred")


def test_open_view(view, rf):
    expected = '<a href="/data_browser/query/app.model/fa+0,fd-1,fn.html?bob__equals=fred&limit=1000">view</a>'
    assert ViewAdmin.open_view(view) == expected


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

    all_fields = [
        field
        for fieldset in res.context[0]["adminform"]
        for line in fieldset
        for field in line
    ]
    for field in all_fields:
        if field.is_readonly and field.field["name"] == "public_link":
            expected = f"http://testserver/data_browser/view/{view.public_slug}.csv"
            assert field.contents() == expected
            break
    else:
        assert False


@pytest.fixture
def get_admin_details(rf):
    def helper(admin_user, obj):
        request = rf.get("/")
        request.user = admin_user
        view_admin = ViewAdmin(View, admin.site)
        fields = set(flatten_fieldsets(view_admin.get_fieldsets(request, obj)))
        read_only = set(view_admin.get_readonly_fields(request, obj))
        assert fields == read_only
        return fields

    return helper


@pytest.fixture
def staff_user(admin_user):
    admin_user.is_superuser = False
    admin_user.user_permissions.add(Permission.objects.get(codename="change_view"))
    return admin_user


class TestAdminFieldsSuperUser:
    def test_add_page_edit_everything(self, admin_user, get_admin_details):
        fields = get_admin_details(admin_user, None)
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
        }

    def test_private_view_edit_everything(self, admin_user, get_admin_details, view):
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
        }

    def test_public_view_edit_everything(self, admin_user, get_admin_details, view):
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
        }


class TestAdminFieldsStaffUser:
    def test_add_page_no_public_fields(self, staff_user, get_admin_details):
        fields = get_admin_details(staff_user, None)
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
        }

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
        }
