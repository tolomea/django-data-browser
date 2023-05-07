import json

import pytest
from django.contrib.auth.models import Permission, User

from data_browser.common import PUBLIC_PERM, SHARE_PERM
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
    return User.objects.create(
        username="other", is_active=True, is_superuser=True, is_staff=True
    )


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


@pytest.fixture
def get_list_summary(admin_client):
    def inner(user, extra_keys=None):
        keys = {"type", "name", "entries"}
        if extra_keys:
            keys.update(extra_keys)

        def summarize(stuff):
            if isinstance(stuff, dict):
                return {k: summarize(v) for k, v in stuff.items() if k in keys}
            elif isinstance(stuff, list):
                return [summarize(x) for x in stuff]
            return stuff

        admin_client.force_login(user)
        resp = admin_client.get("/data_browser/api/views/")
        assert resp.status_code == 200
        res = {
            "saved": summarize(resp.json()["saved"]),
            "shared": summarize(resp.json()["shared"]),
        }
        print(json.dumps(res, indent=4, sort_keys=True))
        return res

    return inner


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
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
        assert resp.json() == {
            "saved": [
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
                    "link": (
                        "/query/core.Product/admin.html?name__contains=sql&limit=1000"
                    ),
                    "createdTime": ANY(str),
                    "pk": view.pk,
                    "limit": 1000,
                    "shared": False,
                    "valid": True,
                    "can_edit": True,
                    "type": "view",
                }
            ],
            "shared": [],
        }

    def test_with_multiple_aut_backends(self, admin_client, admin_user, view, settings):
        settings.AUTHENTICATION_BACKENDS = [
            "django.contrib.auth.backends.ModelBackend",
            "django.contrib.auth.backends.ModelBackend",
        ]

        resp = admin_client.get("/data_browser/api/views/")
        assert resp.status_code == 200

    def test_get_with_folders_and_shared_views(
        self, view, multiple_views, admin_user, other_user, get_list_summary
    ):
        make_view(
            owner=other_user,
            name="shared_in_folder",
            shared=True,
            folder="other folder",
        )
        make_view(owner=other_user, name="shared_out_of_folder", shared=True)

        summary = get_list_summary(admin_user, {"shared", "can_edit"})
        assert summary == {
            "saved": [
                {
                    "type": "folder",
                    "name": "my folder",
                    "entries": [
                        {
                            "name": "my_in_folder",
                            "shared": False,
                            "type": "view",
                            "can_edit": True,
                        }
                    ],
                },
                {
                    "name": "my_out_of_folder",
                    "shared": False,
                    "type": "view",
                    "can_edit": True,
                },
                {"name": "name", "shared": False, "type": "view", "can_edit": True},
            ],
            "shared": [
                {
                    "type": "folder",
                    "name": "other",
                    "entries": [
                        {
                            "name": "other folder",
                            "type": "folder",
                            "entries": [
                                {
                                    "name": "shared_in_folder",
                                    "shared": True,
                                    "type": "view",
                                    "can_edit": False,
                                }
                            ],
                        },
                        {
                            "name": "shared_out_of_folder",
                            "shared": True,
                            "type": "view",
                            "can_edit": False,
                        },
                    ],
                }
            ],
        }

    def test_get_multi_no_sharing(
        self, admin_user, other_user, get_list_summary, multiple_views
    ):
        # admin sees only their own
        summary = get_list_summary(admin_user)
        assert summary == {
            "saved": [
                {
                    "type": "folder",
                    "name": "my folder",
                    "entries": [{"name": "my_in_folder", "type": "view"}],
                },
                {"name": "my_out_of_folder", "type": "view"},
            ],
            "shared": [],
        }

        # other sees only their own
        summary = get_list_summary(other_user)
        assert summary == {
            "saved": [
                {
                    "type": "folder",
                    "name": "other folder",
                    "entries": [{"name": "other_in_folder", "type": "view"}],
                },
                {"name": "other_out_of_folder", "type": "view"},
            ],
            "shared": [],
        }

    def test_get_multi_everything_sharing(
        self, admin_user, other_user, get_list_summary, multiple_views
    ):
        View.objects.update(shared=True)

        # admin sees everything
        summary = get_list_summary(admin_user)
        assert summary == {
            "saved": [
                {
                    "type": "folder",
                    "name": "my folder",
                    "entries": [{"name": "my_in_folder", "type": "view"}],
                },
                {"name": "my_out_of_folder", "type": "view"},
            ],
            "shared": [
                {
                    "entries": [
                        {
                            "entries": [{"name": "other_in_folder", "type": "view"}],
                            "name": "other folder",
                            "type": "folder",
                        },
                        {"name": "other_out_of_folder", "type": "view"},
                    ],
                    "name": "other",
                    "type": "folder",
                }
            ],
        }

        # other sees everything
        summary = get_list_summary(other_user)
        assert summary == {
            "saved": [
                {
                    "type": "folder",
                    "name": "other folder",
                    "entries": [{"name": "other_in_folder", "type": "view"}],
                },
                {"name": "other_out_of_folder", "type": "view"},
            ],
            "shared": [
                {
                    "entries": [
                        {
                            "entries": [{"name": "my_in_folder", "type": "view"}],
                            "name": "my folder",
                            "type": "folder",
                        },
                        {"name": "my_out_of_folder", "type": "view"},
                    ],
                    "name": "admin",
                    "type": "folder",
                }
            ],
        }

    def test_get_multi_everything_sharing_no_perms(
        self, admin_user, other_user, get_list_summary, multiple_views
    ):
        View.objects.update(shared=True)

        # other can share but has no other perms
        other_user.is_superuser = False
        other_user.save()
        other_user.user_permissions.add(*Permission.objects.filter(codename=SHARE_PERM))

        # admin can see others shares
        summary = get_list_summary(admin_user)
        assert summary == {
            "saved": [
                {
                    "type": "folder",
                    "name": "my folder",
                    "entries": [{"name": "my_in_folder", "type": "view"}],
                },
                {"name": "my_out_of_folder", "type": "view"},
            ],
            "shared": [
                {
                    "entries": [
                        {
                            "entries": [{"name": "other_in_folder", "type": "view"}],
                            "name": "other folder",
                            "type": "folder",
                        },
                        {"name": "other_out_of_folder", "type": "view"},
                    ],
                    "name": "other",
                    "type": "folder",
                }
            ],
        }

        # other can only see their own stuff
        summary = get_list_summary(other_user)
        assert summary == {
            "saved": [
                {
                    "type": "folder",
                    "name": "other folder",
                    "entries": [{"name": "other_in_folder", "type": "view"}],
                },
                {"name": "other_out_of_folder", "type": "view"},
            ],
            "shared": [],
        }

    def test_get_multi_everything_no_sharing(
        self, admin_user, other_user, get_list_summary, multiple_views
    ):
        View.objects.update(shared=True)

        # other can do anything but share
        other_user.is_superuser = False
        other_user.save()
        other_user.user_permissions.add(
            *Permission.objects.exclude(codename=SHARE_PERM)
        )

        # admin doesn't see others shares
        summary = get_list_summary(admin_user)
        assert summary == {
            "saved": [
                {
                    "type": "folder",
                    "name": "my folder",
                    "entries": [{"name": "my_in_folder", "type": "view"}],
                },
                {"name": "my_out_of_folder", "type": "view"},
            ],
            "shared": [],
        }

        # other sees everything
        summary = get_list_summary(other_user)
        assert summary == {
            "saved": [
                {
                    "type": "folder",
                    "name": "other folder",
                    "entries": [{"name": "other_in_folder", "type": "view"}],
                },
                {"name": "other_out_of_folder", "type": "view"},
            ],
            "shared": [
                {
                    "entries": [
                        {
                            "entries": [{"name": "my_in_folder", "type": "view"}],
                            "name": "my folder",
                            "type": "folder",
                        },
                        {"name": "my_out_of_folder", "type": "view"},
                    ],
                    "name": "admin",
                    "type": "folder",
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
            "valid": True,
            "can_edit": True,
            "type": "view",
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
            "valid": True,
            "can_edit": True,
            "type": "view",
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
            "valid": True,
            "can_edit": True,
            "type": "view",
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
            "valid": True,
            "can_edit": True,
            "type": "view",
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
