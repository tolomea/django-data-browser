import json

import pytest
from django.contrib.auth.models import Permission, User

from data_browser.common import PUBLIC_PERM
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
    return User.objects.create(username="other", is_active=True, is_superuser=True)


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
def admin_user_limited(admin_user):
    admin_user.is_superuser = False
    admin_user.save()

    admin_user.user_permissions.add(*Permission.objects.exclude(codename=PUBLIC_PERM))
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
        assert resp.json() == {
            "saved": [
                {
                    "name": "",
                    "views": [
                        {
                            "name": "name",
                            "description": "description",
                            "folder": "",
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
                            "shared": False,
                        }
                    ],
                }
            ],
            "shared": [],
        }

    def test_get_with_folders_and_shared_views(
        self, admin_client, admin_user, view, other_user
    ):
        def make_view(**kwargs):
            View.objects.create(
                model_name="core.Product",
                fields="admin",
                query="name__contains=sql",
                **kwargs,
            )

        def get_summary():
            def summarize(stuff):
                keys = {"name", "views", "shared", "saved", "ownerName"}
                if isinstance(stuff, dict):
                    return {k: summarize(v) for k, v in stuff.items() if k in keys}
                elif isinstance(stuff, list):
                    return [summarize(x) for x in stuff]
                return stuff

            resp = admin_client.get("/data_browser/api/views/")
            assert resp.status_code == 200
            return summarize(resp.json())

        make_view(owner=admin_user, name="in_folder", folder="folder")
        make_view(owner=admin_user, name="out_of_folder")
        make_view(owner=other_user, name="other_in_folder", folder="folder")
        make_view(owner=other_user, name="other_out_of_folder")
        make_view(
            owner=other_user, name="shared_in_folder", shared=True, folder="folder"
        )
        make_view(owner=other_user, name="shared_out_of_folder", shared=True)

        assert get_summary() == {
            "saved": [
                {
                    "name": "",
                    "views": [
                        {"name": "name", "shared": False},
                        {"name": "out_of_folder", "shared": False},
                    ],
                },
                {"name": "folder", "views": [{"name": "in_folder", "shared": False}]},
            ],
            "shared": [
                {
                    "ownerName": "other",
                    "views": [
                        {
                            "name": "",
                            "views": [{"name": "shared_out_of_folder", "shared": True}],
                        },
                        {
                            "name": "folder",
                            "views": [{"name": "shared_in_folder", "shared": True}],
                        },
                    ],
                }
            ],
        }

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
            "folder": "",
            "public": True,
            "model": "core.Product",
            "fields": "",
            "query": "",
            "publicLink": link,
            "googleSheetsFormula": f'=importdata("{link}")',
            "link": "/query/core.Product/.html?limit=1000",
            "createdTime": ANY(str),
            "pk": view.pk,
            "limit": 1000,
            "shared": False,
        }

        assert view.owner == admin_user
        assert view.name == "test"
        assert view.description == "lorem ipsum"
        assert view.public
        assert view.model_name == "core.Product"
        assert view.fields == ""
        assert view.query == ""


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
            "folder": "",
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
            "shared": False,
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
            "folder": "",
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
            "shared": False,
        }

        assert view.owner == admin_user
        assert view.name == "test"
        assert view.description == "lorem ipsum"
        assert view.public
        assert view.model_name == "core.Product"
        assert view.fields == "admin"
        assert view.query == "name__contains=sql"
        assert view.limit == 1000

    def test_patch_limit(self, admin_client, admin_user, view):
        resp = admin_client.patch(
            f"/data_browser/api/views/{view.pk}/",
            json.dumps({"limit": "123"}),
            content_type="application/json",
        )
        assert resp.status_code == 200

        view.refresh_from_db()

        assert resp.json() == {
            "name": "name",
            "description": "description",
            "folder": "",
            "public": False,
            "model": "core.Product",
            "fields": "admin",
            "query": "name__contains=sql",
            "publicLink": "N/A",
            "googleSheetsFormula": "N/A",
            "link": "/query/core.Product/admin.html?name__contains=sql&limit=123",
            "createdTime": ANY(str),
            "pk": view.pk,
            "limit": 123,
            "shared": False,
        }

        assert view.owner == admin_user
        assert view.name == "name"
        assert view.description == "description"
        assert not view.public
        assert view.model_name == "core.Product"
        assert view.fields == "admin"
        assert view.query == "name__contains=sql"
        assert view.limit == 123

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

    def test_patch_text_limit(self, admin_client, admin_user_limited, view):
        resp = admin_client.patch(
            f"/data_browser/api/views/{view.pk}/",
            json.dumps({"limit": "bob"}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert not resp.json()["public"]
        view.refresh_from_db()
        assert view.limit == 1

    def test_patch_negative_limit(self, admin_client, admin_user_limited, view):
        resp = admin_client.patch(
            f"/data_browser/api/views/{view.pk}/",
            json.dumps({"limit": -1}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert not resp.json()["public"]
        view.refresh_from_db()
        assert view.limit == 1
