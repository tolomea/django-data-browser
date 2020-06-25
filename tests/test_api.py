import json

import pytest
from data_browser.models import View


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


class TestViewList:
    # can't see other users view
    # can't create public without perm
    # bad methods
    def test_get(self, admin_client, view):
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
        assert resp.json() == {
            "name": "test",
            "description": "lorem ipsum",
            "public": True,
            "model": "core.Product",
            "fields": "",
            "query": "",
        }

        view = View.objects.get()
        assert view.owner == admin_user
        assert view.name == "test"
        assert view.description == "lorem ipsum"
        assert view.public
        assert view.model_name == "core.Product"
        assert view.fields == ""
        assert view.query == ""


class TestViewDetail:
    # can't see other users view
    # can't edit other users view
    # can't delete other users view
    # can't set public without perm
    # bad methods
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
        }

    def test_delete(self, admin_client, view):
        assert View.objects.exists()
        resp = admin_client.delete(f"/data_browser/api/views/{view.pk}/")
        assert resp.status_code == 204
        assert not View.objects.exists()

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
        assert resp.json() == {
            "name": "test",
            "description": "lorem ipsum",
            "public": True,
            "model": "core.Product",
            "fields": "admin",
            "query": "name__contains=sql",
        }

        view.refresh_from_db()
        assert view.owner == admin_user
        assert view.name == "test"
        assert view.description == "lorem ipsum"
        assert view.public
        assert view.model_name == "core.Product"
        assert view.fields == "admin"
        assert view.query == "name__contains=sql"
