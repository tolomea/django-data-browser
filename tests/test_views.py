import csv
import json

import data_browser.models
import pytest
from django.contrib.auth.models import User

from . import models

true = True
false = False
null = None


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
        "/data_browser/query/tests.Product/size-0,name+1,size_unit.html?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    context = json.loads(res.context["ctx"])
    assert context.keys() == {"config", "initialState", "sentryDsn"}

    assert context["initialState"].keys() == {"model", "fields", "filters", "data"}
    assert context["initialState"]["model"] == "tests.Product"
    print(json.dumps(context["initialState"]["fields"], indent=4, sort_keys=True))
    assert context["initialState"]["fields"] == [
        {"path": "size", "priority": 0, "sort": "dsc"},
        {"path": "name", "priority": 1, "sort": "asc"},
        {"path": "size_unit", "priority": null, "sort": null},
    ]
    assert context["initialState"]["filters"] == [
        {"errorMessage": None, "lookup": "lt", "path": "size", "value": "2"},
        {"errorMessage": None, "lookup": "gt", "path": "id", "value": "0"},
    ]
    assert context["initialState"]["data"] == []

    assert context["config"].keys() == {
        "baseUrl",
        "adminUrl",
        "sortedModels",
        "types",
        "allModelFields",
    }
    assert context["config"]["baseUrl"] == "/data_browser/"
    assert context["config"]["adminUrl"] == "/admin/data_browser/view/add/"
    assert context["config"]["sortedModels"] == [
        "auth.Group",
        "auth.User",
        "data_browser.View",
        "tests.Address",
        "tests.InAdmin",
        "tests.InlineAdmin",
        "tests.Normal",
        "tests.Producer",
        "tests.Product",
        "tests.SKU",
        "tests.Tag",
    ]
    print(json.dumps(context["config"]["types"], indent=4, sort_keys=True))
    assert context["config"]["types"] == {
        "boolean": {
            "defaultLookup": "equals",
            "defaultValue": true,
            "lookups": {
                "equals": {"type": "boolean"},
                "is_null": {"type": "boolean"},
                "not_equals": {"type": "boolean"},
            },
            "sortedLookups": ["equals", "not_equals", "is_null"],
        },
        "html": {
            "defaultLookup": null,
            "defaultValue": "",
            "lookups": {},
            "sortedLookups": [],
        },
        "number": {
            "defaultLookup": "equals",
            "defaultValue": 0,
            "lookups": {
                "equals": {"type": "number"},
                "gt": {"type": "number"},
                "gte": {"type": "number"},
                "is_null": {"type": "boolean"},
                "lt": {"type": "number"},
                "lte": {"type": "number"},
                "not_equals": {"type": "number"},
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
        },
        "string": {
            "defaultLookup": "equals",
            "defaultValue": "",
            "lookups": {
                "contains": {"type": "string"},
                "ends_with": {"type": "string"},
                "equals": {"type": "string"},
                "is_null": {"type": "boolean"},
                "not_contains": {"type": "string"},
                "not_ends_with": {"type": "string"},
                "not_equals": {"type": "string"},
                "not_regex": {"type": "string"},
                "not_starts_with": {"type": "string"},
                "regex": {"type": "string"},
                "starts_with": {"type": "string"},
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
        },
        "time": {
            "defaultLookup": "equals",
            "defaultValue": ANY(str),
            "lookups": {
                "equals": {"type": "time"},
                "gt": {"type": "time"},
                "gte": {"type": "time"},
                "is_null": {"type": "boolean"},
                "lt": {"type": "time"},
                "lte": {"type": "time"},
                "not_equals": {"type": "time"},
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
        },
    }
    print(json.dumps(context["config"]["allModelFields"], indent=4, sort_keys=True))
    assert context["config"]["allModelFields"] == {
        "auth.Group": {
            "fields": {
                "admin": {"concrete": false, "type": "html"},
                "id": {"concrete": true, "type": "number"},
                "name": {"concrete": true, "type": "string"},
            },
            "fks": {},
            "sorted_fields": ["id", "admin", "name"],
            "sorted_fks": [],
        },
        "auth.User": {
            "fields": {
                "admin": {"concrete": false, "type": "html"},
                "date_joined": {"concrete": true, "type": "time"},
                "email": {"concrete": true, "type": "string"},
                "first_name": {"concrete": true, "type": "string"},
                "id": {"concrete": true, "type": "number"},
                "is_active": {"concrete": true, "type": "boolean"},
                "is_staff": {"concrete": true, "type": "boolean"},
                "is_superuser": {"concrete": true, "type": "boolean"},
                "last_login": {"concrete": true, "type": "time"},
                "last_name": {"concrete": true, "type": "string"},
                "password": {"concrete": true, "type": "string"},
                "username": {"concrete": true, "type": "string"},
            },
            "fks": {},
            "sorted_fields": [
                "id",
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
        "data_browser.View": {
            "fields": {
                "admin": {"concrete": false, "type": "html"},
                "created_time": {"concrete": true, "type": "time"},
                "description": {"concrete": true, "type": "string"},
                "fields": {"concrete": true, "type": "string"},
                "id": {"concrete": true, "type": "string"},
                "model_name": {"concrete": true, "type": "string"},
                "name": {"concrete": true, "type": "string"},
                "public": {"concrete": true, "type": "boolean"},
                "query": {"concrete": true, "type": "string"},
            },
            "fks": {"owner": {"model": "auth.User"}},
            "sorted_fields": [
                "id",
                "admin",
                "created_time",
                "description",
                "fields",
                "model_name",
                "name",
                "public",
                "query",
            ],
            "sorted_fks": ["owner"],
        },
        "tests.Address": {
            "fields": {
                "admin": {"concrete": false, "type": "html"},
                "city": {"concrete": true, "type": "string"},
                "id": {"concrete": true, "type": "number"},
            },
            "fks": {},
            "sorted_fields": ["id", "admin", "city"],
            "sorted_fks": [],
        },
        "tests.InAdmin": {
            "fields": {
                "admin": {"concrete": false, "type": "html"},
                "id": {"concrete": true, "type": "number"},
                "name": {"concrete": true, "type": "string"},
            },
            "fks": {},
            "sorted_fields": ["id", "admin", "name"],
            "sorted_fks": [],
        },
        "tests.InlineAdmin": {
            "fields": {
                "id": {"concrete": true, "type": "number"},
                "name": {"concrete": true, "type": "string"},
            },
            "fks": {"in_admin": {"model": "tests.InAdmin"}},
            "sorted_fields": ["id", "name"],
            "sorted_fks": ["in_admin"],
        },
        "tests.Normal": {
            "fields": {
                "admin": {"concrete": false, "type": "html"},
                "id": {"concrete": true, "type": "number"},
                "name": {"concrete": true, "type": "string"},
            },
            "fks": {
                "in_admin": {"model": "tests.InAdmin"},
                "inline_admin": {"model": "tests.InlineAdmin"},
            },
            "sorted_fields": ["id", "admin", "name"],
            "sorted_fks": ["in_admin", "inline_admin"],
        },
        "tests.Producer": {
            "fields": {
                "admin": {"concrete": false, "type": "html"},
                "id": {"concrete": true, "type": "number"},
                "name": {"concrete": true, "type": "string"},
            },
            "fks": {"address": {"model": "tests.Address"}},
            "sorted_fields": ["id", "admin", "name"],
            "sorted_fks": ["address"],
        },
        "tests.Product": {
            "fields": {
                "admin": {"concrete": false, "type": "html"},
                "id": {"concrete": true, "type": "number"},
                "is_onsale": {"concrete": false, "type": "string"},
                "name": {"concrete": true, "type": "string"},
                "onsale": {"concrete": true, "type": "boolean"},
                "size": {"concrete": true, "type": "number"},
                "size_unit": {"concrete": true, "type": "string"},
            },
            "fks": {
                "default_sku": {"model": "tests.SKU"},
                "producer": {"model": "tests.Producer"},
            },
            "sorted_fields": [
                "id",
                "admin",
                "is_onsale",
                "name",
                "onsale",
                "size",
                "size_unit",
            ],
            "sorted_fks": ["default_sku", "producer"],
        },
        "tests.SKU": {
            "fields": {
                "admin": {"concrete": false, "type": "html"},
                "id": {"concrete": true, "type": "number"},
                "name": {"concrete": true, "type": "string"},
            },
            "fks": {"product": {"model": "tests.Product"}},
            "sorted_fields": ["id", "admin", "name"],
            "sorted_fks": ["product"],
        },
        "tests.Tag": {
            "fields": {
                "admin": {"concrete": false, "type": "html"},
                "id": {"concrete": true, "type": "number"},
                "name": {"concrete": true, "type": "string"},
            },
            "fks": {},
            "sorted_fields": ["id", "admin", "name"],
            "sorted_fks": [],
        },
    }


@pytest.mark.usefixtures("products")
def test_query_json_bad_fields(admin_client):
    res = admin_client.get(
        "".join(
            [
                "/data_browser/query/tests.Product/",
                "size-0,name+1,size_unit,bob-2,is_onsale,pooducer__name,producer__name.json",
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
        "/data_browser/query/tests.Bob/size-0,name+1,size_unit.html?size__lt=2&id__gt=0"
    )
    assert res.status_code == 404


@pytest.mark.usefixtures("products")
def test_query_csv(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests.Product/size-0,name+1,size_unit.csv?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    rows = list(csv.reader(res.content.decode("utf-8").splitlines()))
    assert rows == [["size", "name", "size_unit"], ["1", "a", "g"], ["1", "b", "g"]]


@pytest.mark.usefixtures("products")
def test_query_json(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests.Product/size-0,name+1,size_unit.json?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    data = json.loads(res.content.decode("utf-8"))

    print(json.dumps(data, indent=4, sort_keys=True))
    assert data == {
        "data": [[1, "a", "g"], [1, "b", "g"]],
        "fields": [
            {"path": "size", "priority": 0, "sort": "dsc"},
            {"path": "name", "priority": 1, "sort": "asc"},
            {"path": "size_unit", "priority": null, "sort": null},
        ],
        "filters": [
            {"errorMessage": null, "lookup": "lt", "path": "size", "value": "2"},
            {"errorMessage": null, "lookup": "gt", "path": "id", "value": "0"},
        ],
        "model": "tests.Product",
    }


@pytest.mark.usefixtures("products")
def test_query_json_bad_model(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests.Bob/size-0,name+1,size_unit.json?size__lt=2&id__gt=0"
    )
    assert res.status_code == 404


@pytest.mark.usefixtures("products")
def test_view_csv(admin_client):
    view = data_browser.models.View.objects.create(
        model_name="tests.Product",
        fields="size-0,name+1,size_unit",
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
        fields="size-0,name+1,size_unit",
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
    print(json.dumps(data, indent=4, sort_keys=True))
    assert data == {
        "data": [[1, "a", "g"], [1, "b", "g"]],
        "fields": [
            {"path": "size", "priority": 0, "sort": "dsc"},
            {"path": "name", "priority": 1, "sort": "asc"},
            {"path": "size_unit", "priority": null, "sort": null},
        ],
        "filters": [
            {"errorMessage": null, "lookup": "lt", "path": "size", "value": "2"},
            {"errorMessage": null, "lookup": "gt", "path": "id", "value": "0"},
        ],
        "model": "tests.Product",
    }
