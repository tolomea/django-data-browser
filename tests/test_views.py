import csv
import json

import data_browser.models
import pytest
from data_browser import views
from data_browser.query import BoundQuery, Query
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


@pytest.fixture
def admin_fields(rf, admin_user):
    request = rf.get("/")
    request.user = admin_user
    return views.get_all_admin_fields(request)


@pytest.fixture
def all_model_fields(admin_fields):
    return views.get_all_model_fields(admin_fields)


@pytest.fixture
def get_query_data(all_model_fields, django_assert_num_queries):
    def helper(queries, *args):
        query = Query.from_request(*args)

        bound_query = BoundQuery(
            query, views.get_model(query.app, query.model), all_model_fields
        )
        with django_assert_num_queries(queries):
            return views.get_data(bound_query)

    yield helper


@pytest.fixture
def get_product_data(get_query_data):
    return lambda queries, *args, **kwargs: get_query_data(
        queries, "tests", "product", *args, **kwargs
    )


@pytest.mark.usefixtures("products")
def test_get_data_all(get_product_data):
    data = get_product_data(1, "-size,+name,size_unit", "html", {})
    assert data == [[2, "c", "g"], [1, "a", "g"], [1, "b", "g"]]


@pytest.mark.usefixtures("products")
def test_get_data_empty(get_product_data):
    data = get_product_data(0, "", "html", {})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_data_sort(get_product_data):
    data = get_product_data(1, "+size,-name,size_unit", "html", {})
    assert data == [[1, "b", "g"], [1, "a", "g"], [2, "c", "g"]]


@pytest.mark.usefixtures("products")
def test_get_data_pks(get_product_data):
    data = get_product_data(1, "pk", "html", {})
    assert {d[0] for d in data} == set(
        models.Product.objects.values_list("pk", flat=True)
    )


@pytest.mark.usefixtures("products")
def test_get_data_calculated_field(get_product_data):
    # query + prefetch producer
    data = get_product_data(2, "+name,producer__name,is_onsale", "html", {})
    assert data == [["a", "Bob", False], ["b", "Bob", False], ["c", "Bob", False]]


@pytest.mark.usefixtures("products")
def test_get_data_filtered(get_product_data):
    data = get_product_data(1, "size,name", "html", {"name__equals": ["a"]})
    assert data == [[1, "a"]]


@pytest.mark.usefixtures("products")
def test_get_data_excluded(get_product_data):
    data = get_product_data(1, "-size,name", "html", {"name__not_equals": ["a"]})
    assert data == [[2, "c"], [1, "b"]]


@pytest.mark.usefixtures("products")
def test_get_data_multi_excluded(get_product_data):
    data = get_product_data(1, "-size,name", "html", {"name__not_equals": ["a", "c"]})
    assert data == [[1, "b"]]


@pytest.mark.usefixtures("products")
def test_get_data_collapsed(get_product_data):
    data = get_product_data(1, "-size,size_unit", "html", {})
    assert data == [[2, "g"], [1, "g"]]


@pytest.mark.usefixtures("products")
def test_get_data_null_filter(get_product_data):
    data = get_product_data(1, "pk", "html", {"onsale__is_null": ["True"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "pk", "html", {"onsale__is_null": ["true"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "pk", "html", {"onsale__is_null": ["False"]})
    assert data == []
    data = get_product_data(1, "pk", "html", {"onsale__is_null": ["false"]})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_data_boolean_filter(get_product_data):
    models.Product.objects.update(onsale=True)
    data = get_product_data(1, "pk", "html", {"onsale__equals": ["True"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "pk", "html", {"onsale__equals": ["true"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "pk", "html", {"onsale__equals": ["False"]})
    assert data == []
    data = get_product_data(1, "pk", "html", {"onsale__equals": ["false"]})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_data_string_filter(get_product_data):
    data = get_product_data(1, "pk", "html", {"producer__name__equals": ["Bob"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "pk", "html", {"producer__name__equals": ["bob"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "pk", "html", {"producer__name__equals": ["fred"]})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_data_prefetch(get_product_data):
    # query products, prefetch producer, producer__address
    data = get_product_data(3, "+name,is_onsale,producer__address__city", "html", {})
    assert data == [
        ["a", False, "london"],
        ["b", False, "london"],
        ["c", False, "london"],
    ]


@pytest.mark.usefixtures("products")
def test_get_data_prefetch_with_filter(get_product_data):
    # query products, join to producer, producer__address
    data = get_product_data(
        1,
        "+name,is_onsale,producer__address__city",
        "html",
        {"producer__address__city__not_equals": ["Invercargill"]},
    )
    assert data == [
        ["a", False, "london"],
        ["b", False, "london"],
        ["c", False, "london"],
    ]


@pytest.mark.usefixtures("products")
def test_get_data_no_calculated_so_flat(get_product_data):
    # query products, join the rest
    data = get_product_data(1, "+name,producer__address__city", "html", {})
    assert data == [["a", "london"], ["b", "london"], ["c", "london"]]


@pytest.mark.usefixtures("products")
def test_get_data_sort_causes_select(get_product_data):
    # query products, join the rest
    data = get_product_data(1, "+name,is_onsale,-producer__address__city", "html", {})
    assert data == [
        ["a", False, "london"],
        ["b", False, "london"],
        ["c", False, "london"],
    ]


@pytest.mark.usefixtures("products")
def test_get_data_filter_causes_select(get_product_data):
    # query products, join the rest
    data = get_product_data(
        1,
        "+name,is_onsale,producer__address__city",
        "html",
        {"producer__address__city__equals": ["london"]},
    )
    assert data == [
        ["a", False, "london"],
        ["b", False, "london"],
        ["c", False, "london"],
    ]


def test_get_fields(all_model_fields):
    # basic
    assert "name" in all_model_fields[models.Product]["fields"]

    # remap id to pk
    assert "id" not in all_model_fields[models.Product]["fields"]
    assert "pk" in all_model_fields[models.Product]["fields"]

    # follow fk
    assert "producer" not in all_model_fields[models.Product]["fields"]
    assert "producer" in all_model_fields[models.Product]["fks"]
    assert "name" in all_model_fields[models.Producer]["fields"]

    # follow multiple fk's
    assert "city" in all_model_fields[models.Address]["fields"]

    # no many to many fields
    assert "tags" not in all_model_fields[models.Product]["fields"]

    # check in and out of admin
    assert "not_in_admin" not in all_model_fields[models.Product]["fields"]
    assert "fk_not_in_admin" not in all_model_fields[models.Product]["fks"]
    assert "model_not_in_admin" in all_model_fields[models.Product]["fks"]
    assert models.NotInAdmin not in all_model_fields


def test_query_html(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests.Product/-size,+name,size_unit.html?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    context = json.loads(res.context["data"])
    assert context.keys() == {"model", "baseUrl", "adminUrl", "types", "allModelFields"}
    assert context["model"] == "tests.Product"
    assert context["baseUrl"] == "/data_browser/"
    assert context["adminUrl"] == "/admin/data_browser/view/add/"

    true = True
    false = False
    null = None

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
                "model": {"type": "string", "concrete": true},
                "query": {"type": "string", "concrete": true},
                "app": {"type": "string", "concrete": true},
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
                "app",
                "created_time",
                "description",
                "fields",
                "id",
                "model",
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
        "/data_browser/query/tests.Product/-size,+name,size_unit,-bob,is_onsale,pooducer__name,producer__name.json?size__lt=2&id__gt=0&bob__gt=1&size__xx=1&size__lt=xx"
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
    assert res.status_code == 200
    assert res.content == b"App 'tests' doesn't have a 'Bob' model."


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
            {"errorMessage": None, "name": "size", "lookup": "lt", "value": "2"}
        ],
        "fields": [
            {"name": "size", "sort": "dsc"},
            {"name": "name", "sort": "asc"},
            {"name": "size_unit", "sort": None},
        ],
    }


@pytest.mark.usefixtures("products")
def test_view_csv(admin_client):
    view = data_browser.models.View.objects.create(
        app="tests",
        model="Product",
        fields="-size,+name,size_unit",
        query='{"size__lt": ["2"], "id__gt": ["0"]}',
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
        app="tests",
        model="Product",
        fields="-size,+name,size_unit",
        query='{"size__lt": ["2"], "id__gt": ["0"]}',
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
            {"errorMessage": None, "name": "size", "lookup": "lt", "value": "2"}
        ],
        "fields": [
            {"name": "size", "sort": "dsc"},
            {"name": "name", "sort": "asc"},
            {"name": "size_unit", "sort": None},
        ],
    }


# TODO calculated field, on admin, on model, both
# TODO missing permissions
# TODO view owner missing permissions
