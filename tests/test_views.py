import csv
import json

import data_browser.models
import pytest
from django.contrib.auth.models import User

from . import models


class ANY:  # pragma: no cover
    def __init__(self, type):
        self.type = type

    def __eq__(self, other):
        return isinstance(other, self.type)


@pytest.fixture
def products(db):
    address = models.Address.objects.create(city="london")
    producer = models.Producer.objects.create(name="Bob", address=address)
    models.Product.objects.create(name="a", size=1, size_unit="g", producer=producer)
    models.Product.objects.create(name="b", size=1, size_unit="g", producer=producer)
    models.Product.objects.create(name="c", size=2, size_unit="g", producer=producer)


def test_query_html(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests.Product/-size,+name,size_unit.html?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    context = json.loads(res.context["ctx"])
    assert context.keys() == {
        "model",
        "baseUrl",
        "adminUrl",
        "filters",
        "fields",
        "types",
        "allModelFields",
        "sortedModels",
    }
    assert context["model"] == "tests.Product"
    assert context["baseUrl"] == "/data_browser/"
    assert context["adminUrl"] == "/admin/data_browser/view/add/"
    assert context["sortedModels"] == [
        "auth.Group",
        "auth.User",
        "data_browser.View",
        "tests.Address",
        "tests.InAdmin",
        "tests.Producer",
        "tests.Product",
        "tests.SKU",
        "tests.Tag",
    ]

    true = True
    false = False
    null = None

    print(json.dumps(context["filters"], indent=4))
    assert context["filters"] == [
        {"errorMessage": null, "path": "size", "lookup": "lt", "value": "2"}
    ]

    print(json.dumps(context["fields"], indent=4))
    assert context["fields"] == [
        {"path": "size", "sort": "dsc"},
        {"path": "name", "sort": "asc"},
        {"path": "size_unit", "sort": null},
    ]

    print(json.dumps(context["types"], indent=4))
    assert context["types"] == {
        "string": {
            "lookups": {
                "equals": {"type": "string"},
                "contains": {"type": "string"},
                "starts_with": {"type": "string"},
                "ends_with": {"type": "string"},
                "regex": {"type": "string"},
                "not_equals": {"type": "string"},
                "not_contains": {"type": "string"},
                "not_starts_with": {"type": "string"},
                "not_ends_with": {"type": "string"},
                "not_regex": {"type": "string"},
                "is_null": {"type": "boolean"},
            },
            "sortedLookups": [
                "equals",
                "contains",
                "starts_with",
                "ends_with",
                "regex",
                "not_equals",
                "not_contains",
                "not_starts_with",
                "not_ends_with",
                "not_regex",
                "is_null",
            ],
            "defaultLookup": "equals",
            "defaultValue": "",
        },
        "number": {
            "lookups": {
                "equals": {"type": "number"},
                "not_equals": {"type": "number"},
                "gt": {"type": "number"},
                "gte": {"type": "number"},
                "lt": {"type": "number"},
                "lte": {"type": "number"},
                "is_null": {"type": "boolean"},
            },
            "sortedLookups": [
                "equals",
                "not_equals",
                "gt",
                "gte",
                "lt",
                "lte",
                "is_null",
            ],
            "defaultLookup": "equals",
            "defaultValue": 0,
        },
        "time": {
            "lookups": {
                "equals": {"type": "time"},
                "not_equals": {"type": "time"},
                "gt": {"type": "time"},
                "gte": {"type": "time"},
                "lt": {"type": "time"},
                "lte": {"type": "time"},
                "is_null": {"type": "boolean"},
            },
            "sortedLookups": [
                "equals",
                "not_equals",
                "gt",
                "gte",
                "lt",
                "lte",
                "is_null",
            ],
            "defaultLookup": "equals",
            "defaultValue": ANY(str),
        },
        "boolean": {
            "lookups": {
                "equals": {"type": "boolean"},
                "not_equals": {"type": "boolean"},
                "is_null": {"type": "boolean"},
            },
            "sortedLookups": ["equals", "not_equals", "is_null"],
            "defaultLookup": "equals",
            "defaultValue": true,
        },
        "html": {
            "lookups": {},
            "sortedLookups": [],
            "defaultLookup": null,
            "defaultValue": "",
        },
    }

    print(json.dumps(context["allModelFields"], indent=4))
    assert context["allModelFields"] == {
        "auth.Group": {
            "fields": {
                "admin": {"type": "html", "concrete": false},
                "name": {"type": "string", "concrete": true},
                "pk": {"type": "number", "concrete": true},
            },
            "fks": {},
            "sorted_fields": ["pk", "admin", "name"],
            "sorted_fks": [],
        },
        "auth.User": {
            "fields": {
                "admin": {"type": "html", "concrete": false},
                "date_joined": {"type": "time", "concrete": true},
                "is_staff": {"type": "boolean", "concrete": true},
                "pk": {"type": "number", "concrete": true},
                "last_login": {"type": "time", "concrete": true},
                "is_superuser": {"type": "boolean", "concrete": true},
                "first_name": {"type": "string", "concrete": true},
                "email": {"type": "string", "concrete": true},
                "username": {"type": "string", "concrete": true},
                "last_name": {"type": "string", "concrete": true},
                "is_active": {"type": "boolean", "concrete": true},
                "password": {"type": "string", "concrete": true},
            },
            "fks": {},
            "sorted_fields": [
                "pk",
                "admin",
                "date_joined",
                "email",
                "first_name",
                "is_active",
                "is_staff",
                "is_superuser",
                "last_login",
                "last_name",
                "password",
                "username",
            ],
            "sorted_fks": [],
        },
        "tests.InAdmin": {
            "fields": {
                "admin": {"type": "html", "concrete": false},
                "name": {"type": "string", "concrete": true},
                "pk": {"type": "number", "concrete": true},
            },
            "fks": {},
            "sorted_fields": ["pk", "admin", "name"],
            "sorted_fks": [],
        },
        "tests.Tag": {
            "fields": {
                "admin": {"type": "html", "concrete": false},
                "name": {"type": "string", "concrete": true},
                "pk": {"type": "number", "concrete": true},
            },
            "fks": {},
            "sorted_fields": ["pk", "admin", "name"],
            "sorted_fks": [],
        },
        "tests.Address": {
            "fields": {
                "admin": {"type": "html", "concrete": false},
                "pk": {"type": "number", "concrete": true},
                "city": {"type": "string", "concrete": true},
            },
            "fks": {},
            "sorted_fields": ["pk", "admin", "city"],
            "sorted_fks": [],
        },
        "tests.Producer": {
            "fields": {
                "admin": {"type": "html", "concrete": false},
                "name": {"type": "string", "concrete": true},
                "pk": {"type": "number", "concrete": true},
            },
            "fks": {"address": {"model": "tests.Address"}},
            "sorted_fields": ["pk", "admin", "name"],
            "sorted_fks": ["address"],
        },
        "tests.Product": {
            "fields": {
                "admin": {"type": "html", "concrete": false},
                "is_onsale": {"type": "string", "concrete": false},
                "size_unit": {"type": "string", "concrete": true},
                "pk": {"type": "number", "concrete": true},
                "onsale": {"type": "boolean", "concrete": true},
                "name": {"type": "string", "concrete": true},
                "size": {"type": "number", "concrete": true},
            },
            "fks": {
                "default_sku": {"model": "tests.SKU"},
                "producer": {"model": "tests.Producer"},
                "model_not_in_admin": {"model": "tests.NotInAdmin"},
            },
            "sorted_fields": [
                "pk",
                "admin",
                "is_onsale",
                "name",
                "onsale",
                "size",
                "size_unit",
            ],
            "sorted_fks": ["default_sku", "model_not_in_admin", "producer"],
        },
        "tests.SKU": {
            "fields": {
                "admin": {"type": "html", "concrete": false},
                "name": {"type": "string", "concrete": true},
                "pk": {"type": "number", "concrete": true},
            },
            "fks": {"product": {"model": "tests.Product"}},
            "sorted_fields": ["pk", "admin", "name"],
            "sorted_fks": ["product"],
        },
        "data_browser.View": {
            "fields": {
                "admin": {"type": "html", "concrete": false},
                "model_name": {"type": "string", "concrete": true},
                "query": {"type": "string", "concrete": true},
                "id": {"type": "string", "concrete": true},
                "pk": {"type": "string", "concrete": true},
                "name": {"type": "string", "concrete": true},
                "created_time": {"type": "time", "concrete": true},
                "fields": {"type": "string", "concrete": true},
                "description": {"type": "string", "concrete": true},
                "public": {"type": "boolean", "concrete": true},
            },
            "fks": {"owner": {"model": "auth.User"}},
            "sorted_fields": [
                "pk",
                "admin",
                "created_time",
                "description",
                "fields",
                "id",
                "model_name",
                "name",
                "public",
                "query",
            ],
            "sorted_fks": ["owner"],
        },
    }


@pytest.mark.usefixtures("products")
def test_query_json_bad_fields(admin_client):
    res = admin_client.get(
        "".join(
            [
                "/data_browser/query/tests.Product/",
                "-size,+name,size_unit,-bob,is_onsale,pooducer__name,producer__name.json",
                "?size__lt=2&id__gt=0&bob__gt=1&size__xx=1&size__lt=xx",
            ]
        )
    )
    assert res.status_code == 200
    assert json.loads(res.content.decode("utf-8"))["data"] == [
        [1, "a", "g", False, "Bob"],
        [1, "b", "g", False, "Bob"],
    ]


def test_query_html_bad_model(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests.Bob/-size,+name,size_unit.html?size__lt=2&id__gt=0"
    )
    assert res.status_code == 404


@pytest.mark.usefixtures("products")
def test_query_csv(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests.Product/-size,+name,size_unit.csv?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    rows = list(csv.reader(res.content.decode("utf-8").splitlines()))
    assert rows == [["size", "name", "size_unit"], ["1", "a", "g"], ["1", "b", "g"]]


@pytest.mark.usefixtures("products")
def test_query_json(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests.Product/-size,+name,size_unit.json?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    data = json.loads(res.content.decode("utf-8"))

    assert data == {
        "data": [[1, "a", "g"], [1, "b", "g"]],
        "filters": [
            {"errorMessage": None, "path": "size", "lookup": "lt", "value": "2"}
        ],
        "fields": [
            {"path": "size", "sort": "dsc"},
            {"path": "name", "sort": "asc"},
            {"path": "size_unit", "sort": None},
        ],
        "model": "tests.Product",
    }


@pytest.mark.usefixtures("products")
def test_query_json_bad_model(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests.Bob/-size,+name,size_unit.json?size__lt=2&id__gt=0"
    )
    assert res.status_code == 404


@pytest.mark.usefixtures("products")
def test_view_csv(admin_client):
    view = data_browser.models.View.objects.create(
        model_name="tests.Product",
        fields="-size,+name,size_unit",
        query="size__lt=2&id__gt=0",
        owner=User.objects.get(),
    )

    res = admin_client.get(f"/data_browser/view/{view.pk}.csv")
    assert res.status_code == 404

    view.public = True
    view.save()
    res = admin_client.get(f"/data_browser/view/{view.pk}.csv")
    assert res.status_code == 200
    rows = list(csv.reader(res.content.decode("utf-8").splitlines()))
    assert rows == [["size", "name", "size_unit"], ["1", "a", "g"], ["1", "b", "g"]]


@pytest.mark.usefixtures("products")
def test_view_json(admin_client):
    view = data_browser.models.View.objects.create(
        model_name="tests.Product",
        fields="-size,+name,size_unit",
        query="size__lt=2&id__gt=0",
        owner=User.objects.get(),
    )

    res = admin_client.get(f"/data_browser/view/{view.pk}.json")
    assert res.status_code == 404

    view.public = True
    view.save()
    res = admin_client.get(f"/data_browser/view/{view.pk}.json")
    assert res.status_code == 200
    data = json.loads(res.content.decode("utf-8"))
    assert data == {
        "data": [[1, "a", "g"], [1, "b", "g"]],
        "filters": [
            {"errorMessage": None, "path": "size", "lookup": "lt", "value": "2"}
        ],
        "fields": [
            {"path": "size", "sort": "dsc"},
            {"path": "name", "sort": "asc"},
            {"path": "size_unit", "sort": None},
        ],
        "model": "tests.Product",
    }
