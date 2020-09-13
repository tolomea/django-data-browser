import json

import pytest
from django.contrib.auth.models import Permission, User

from data_browser.common import MAKE_PUBLIC_CODENAME
from data_browser.models import View

from .util import ANY


@pytest.fixture
def view(admin_user):
    return View.objects.create(
        owner=admin_user,
        name="name",
        description="description",
        public=False,
        model_name="core.Product",
        fields="admin",
        query="name__contains=sql",
    )


@pytest.fixture
def other_user():
    return User.objects.create()


@pytest.fixture
def other_view(other_user):
    return View.objects.create(
        owner=other_user,
        name="name2",
        description="description2",
        public=False,
        model_name="core.Product",
        fields="admin",
        query="name__contains=sql",
    )


@pytest.fixture
def limited_user(admin_user):
    admin_user.is_superuser = False
    admin_user.save()

    admin_user.user_permissions.add(
        *Permission.objects.exclude(codename=MAKE_PUBLIC_CODENAME)
    )
    return admin_user


class TestViewList:
    def test_bad_methods(self, admin_client):
        resp = admin_client.patch("/data_browser/api/views/")
        assert resp.status_code == 400
        resp = admin_client.put("/data_browser/api/views/")
        assert resp.status_code == 400
        resp = admin_client.delete("/data_browser/api/views/")
        assert resp.status_code == 400

    def test_get(self, admin_client, view, other_view):
        resp = admin_client.get("/data_browser/api/views/")
        assert resp.status_code == 200
        assert resp.json() == [
            {
                "name": "name",
                "description": "description",
                "public": False,
                "model": "core.Product",
                "fields": "admin",
                "query": "name__contains=sql",
                "publicLink": "N/A",
                "googleSheetsFormula": "N/A",
                "link": "/query/core.Product/admin.html?name__contains=sql&limit=1000",
                "createdTime": ANY(str),
                "pk": view.pk,
                "limit": 1000,
            }
        ]

    def test_post(self, admin_client, admin_user):
        resp = admin_client.post(
            "/data_browser/api/views/",
            json.dumps(
                {
                    "name": "test",
                    "description": "lorem ipsum",
                    "public": True,
                    "model": "core.Product",
                    # leave the last two out just cause
                }
            ),
            content_type="application/json",
        )
        assert resp.status_code == 200

        view = View.objects.get()
        link = f"http://testserver/data_browser/view/{view.public_slug}.csv"

        assert resp.json() == {
            "name": "test",
            "description": "lorem ipsum",
            "public": True,
            "model": "core.Product",
            "fields": "",
            "query": "",
            "publicLink": link,
            "googleSheetsFormula": f'=importdata("{link}")',
            "link": "/query/core.Product/.html?&limit=1000",
            "createdTime": ANY(str),
            "pk": view.pk,
            "limit": 1000,
        }

        assert view.owner == admin_user
        assert view.name == "test"
        assert view.description == "lorem ipsum"
        assert view.public
        assert view.model_name == "core.Product"
        assert view.fields == ""
        assert view.query == ""

    def test_post_cant_make_public_without_perm(self, admin_client, limited_user):
        resp = admin_client.post(
            "/data_browser/api/views/",
            json.dumps(
                {
                    "name": "test",
                    "description": "lorem ipsum",
                    "public": True,
                    "model": "core.Product",
                    # leave the last two out just cause
                }
            ),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert not resp.json()["public"]
        view = View.objects.get()
        assert not view.public


class TestViewDetail:
    # can't see other users view

    def test_bad_methods(self, admin_client, view):
        resp = admin_client.post(f"/data_browser/api/views/{view.pk}/")
        assert resp.status_code == 400
        resp = admin_client.put(f"/data_browser/api/views/{view.pk}/")
        assert resp.status_code == 400

    def test_get(self, admin_client, view):
        resp = admin_client.get(f"/data_browser/api/views/{view.pk}/")
        assert resp.status_code == 200
        assert resp.json() == {
            "name": "name",
            "description": "description",
            "public": False,
            "model": "core.Product",
            "fields": "admin",
            "query": "name__contains=sql",
            "publicLink": "N/A",
            "googleSheetsFormula": "N/A",
            "link": "/query/core.Product/admin.html?name__contains=sql&limit=1000",
            "createdTime": ANY(str),
            "pk": view.pk,
            "limit": 1000,
        }

    def test_get_other_owner(self, admin_client, other_view):
        resp = admin_client.get(f"/data_browser/api/views/{other_view.pk}/")
        assert resp.status_code == 404

    def test_delete(self, admin_client, view):
        assert View.objects.exists()
        resp = admin_client.delete(f"/data_browser/api/views/{view.pk}/")
        assert resp.status_code == 204
        assert not View.objects.exists()

    def test_delete_other_owner(self, admin_client, other_view):
        assert View.objects.exists()
        resp = admin_client.delete(f"/data_browser/api/views/{other_view.pk}/")
        assert resp.status_code == 404
        other_view.refresh_from_db()

    def test_patch(self, admin_client, admin_user, view):
        resp = admin_client.patch(
            f"/data_browser/api/views/{view.pk}/",
            json.dumps(
                {
                    "name": "test",
                    "description": "lorem ipsum",
                    "public": True,
                    "model": "core.Product",
                    # leave the last two out just cause
                }
            ),
            content_type="application/json",
        )
        assert resp.status_code == 200

        view.refresh_from_db()
        link = f"http://testserver/data_browser/view/{view.public_slug}.csv"

        assert resp.json() == {
            "name": "test",
            "description": "lorem ipsum",
            "public": True,
            "model": "core.Product",
            "fields": "admin",
            "query": "name__contains=sql",
            "publicLink": link,
            "googleSheetsFormula": f'=importdata("{link}")',
            "link": "/query/core.Product/admin.html?name__contains=sql&limit=1000",
            "createdTime": ANY(str),
            "pk": view.pk,
            "limit": 1000,
        }

        assert view.owner == admin_user
        assert view.name == "test"
        assert view.description == "lorem ipsum"
        assert view.public
        assert view.model_name == "core.Product"
        assert view.fields == "admin"
        assert view.query == "name__contains=sql"

    def test_patch_other_owner(self, admin_client, other_user, other_view):
        resp = admin_client.patch(
            f"/data_browser/api/views/{other_view.pk}/",
            json.dumps({"name": "test", "description": "lorem ipsum"}),
            content_type="application/json",
        )
        assert resp.status_code == 404
        other_view.refresh_from_db()
        assert other_view.owner == other_user
        assert other_view.name == "name2"
        assert other_view.description == "description2"

    def test_patch_cant_make_public_without_perm(
        self, admin_client, limited_user, view
    ):
        resp = admin_client.patch(
            f"/data_browser/api/views/{view.pk}/",
            json.dumps({"public": True}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert not resp.json()["public"]
        view.refresh_from_db()
        assert not view.public

    def test_patch_text_limit(self, admin_client, limited_user, view):
        resp = admin_client.patch(
            f"/data_browser/api/views/{view.pk}/",
            json.dumps({"limit": "bob"}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert not resp.json()["public"]
        view.refresh_from_db()
        assert view.limit == 1

    def test_patch_negative_limit(self, admin_client, limited_user, view):
        resp = admin_client.patch(
            f"/data_browser/api/views/{view.pk}/",
            json.dumps({"limit": -1}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert not resp.json()["public"]
        view.refresh_from_db()
        assert view.limit == 1
