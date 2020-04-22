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
    producer = models.Producer.objects.create(name="bob", address=address)
    models.Product.objects.create(name="a", size=1, size_unit="g", producer=producer)
    models.Product.objects.create(name="b", size=1, size_unit="g", producer=producer)
    models.Product.objects.create(name="c", size=2, size_unit="g", producer=producer)


@pytest.fixture
def fields(rf, admin_user):
    request = rf.get("/")
    request.user = admin_user
    admin_fields = views.get_all_admin_fields(request)
    return views.get_nested_fields_for_model(models.Product, admin_fields)


@pytest.fixture
def get_query_data(fields, django_assert_num_queries):
    def helper(queries, *args):
        query = Query.from_request(*args)
        bound_query = BoundQuery(query, fields)
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
def test_get_empty(get_product_data):
    data = get_product_data(0, "", "html", {})
    assert data == []


@pytest.mark.usefixtures("products")
def test_sort(get_product_data):
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
    assert data == [["a", "bob", False], ["b", "bob", False], ["c", "bob", False]]


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
    data = get_product_data(1, "pk", "html", {"onsale__equal": ["True"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "pk", "html", {"onsale__equal": ["true"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "pk", "html", {"onsale__equal": ["False"]})
    assert data == []
    data = get_product_data(1, "pk", "html", {"onsale__equal": ["false"]})
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


def test_get_fields(fields):
    fields, groups = fields

    # basic
    assert "name" in fields

    # remap id to pk
    assert "id" not in fields
    assert "pk" in fields

    # follow fk
    assert "producer" not in fields
    assert "producer" in groups
    assert "name" in groups["producer"][0]

    # follow multiple fk's
    assert "city" in groups["producer"][1]["address"][0]

    # no loops
    assert "product" not in groups["default_sku"][1]

    # no many to many fields
    assert "tags" not in fields

    # check in and out of admin
    assert "not_in_admin" not in fields
    assert "fk_not_in_admin" not in groups
    assert "model_not_in_admin" in groups
    assert groups["model_not_in_admin"] == ({}, {})


@pytest.mark.usefixtures("products")
def test_query_html(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests/Product/-size,+name,size_unit.html?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    context = json.loads(res.context["data"])
    assert context.keys() == {"model", "allFields", "baseUrl", "adminUrl", "app"}
    assert context["model"] == "Product"
    assert context["app"] == "tests"
    assert context["baseUrl"] == "/data_browser/"
    assert context["adminUrl"] == "/admin/data_browser/view/add/"

    assert context["allFields"] == {
        "fields": [
            {"name": "is_onsale", "concrete": False, "lookups": []},
            {
                "name": "name",
                "concrete": True,
                "lookups": [
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
            {
                "name": "onsale",
                "concrete": True,
                "lookups": ["equal", "not_equal", "is_null"],
            },
            {
                "name": "pk",
                "concrete": True,
                "lookups": ["equal", "not_equal", "gt", "gte", "lt", "lte", "is_null"],
            },
            {
                "name": "size",
                "concrete": True,
                "lookups": ["equal", "not_equal", "gt", "gte", "lt", "lte", "is_null"],
            },
            {
                "name": "size_unit",
                "concrete": True,
                "lookups": [
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
        ],
        "fks": [
            {
                "name": "default_sku",
                "path": "default_sku",
                "fields": [
                    {
                        "name": "name",
                        "concrete": True,
                        "lookups": [
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
                    }
                ],
                "fks": [],
            },
            {
                "name": "model_not_in_admin",
                "path": "model_not_in_admin",
                "fields": [],
                "fks": [],
            },
            {
                "name": "producer",
                "path": "producer",
                "fields": [
                    {
                        "name": "name",
                        "concrete": True,
                        "lookups": [
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
                    }
                ],
                "fks": [
                    {
                        "name": "address",
                        "path": "producer__address",
                        "fields": [
                            {
                                "name": "city",
                                "concrete": True,
                                "lookups": [
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
                            }
                        ],
                        "fks": [],
                    }
                ],
            },
        ],
    }


@pytest.mark.usefixtures("products")
def test_query_html_bad_fields(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests/Product/-size,+name,size_unit,-bob,is_onsale.html?size__lt=2&id__gt=0&bob__gt=1&size__xx=1&size__lt=xx"
    )
    assert res.status_code == 200


@pytest.mark.usefixtures("products")
def test_query_json_bad_fields(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests/Product/-size,+name,size_unit,-bob,is_onsale.json?size__lt=2&id__gt=0&bob__gt=1&size__xx=1&size__lt=xx"
    )
    assert res.status_code == 200
    assert json.loads(res.content.decode("utf-8"))["data"] == [
        [1, "a", "g", False],
        [1, "b", "g", False],
    ]


@pytest.mark.usefixtures("products")
def test_query_html_bad_model(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests/Bob/-size,+name,size_unit.html?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    assert res.content == b"App 'tests' doesn't have a 'Bob' model."


@pytest.mark.usefixtures("products")
def test_query_csv(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests/Product/-size,+name,size_unit.csv?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    rows = list(csv.reader(res.content.decode("utf-8").splitlines()))
    assert rows == [["size", "name", "size_unit"], ["1", "a", "g"], ["1", "b", "g"]]


@pytest.mark.usefixtures("products")
def test_query_json(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests/Product/-size,+name,size_unit.json?size__lt=2&id__gt=0"
    )
    assert res.status_code == 200
    data = json.loads(res.content.decode("utf-8"))
    assert data == {
        "data": [[1, "a", "g"], [1, "b", "g"]],
        "filters": [
            {"errorMessage": None, "name": "size", "lookup": "lt", "value": "2"}
        ],
        "fields": [
            {"name": "size", "sort": "dsc", "concrete": True},
            {"name": "name", "sort": "asc", "concrete": True},
            {"name": "size_unit", "sort": None, "concrete": True},
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
            {"name": "size", "sort": "dsc", "concrete": True},
            {"name": "name", "sort": "asc", "concrete": True},
            {"name": "size_unit", "sort": None, "concrete": True},
        ],
    }


# TODO calculated field, on admin, on model, both
# TODO missing permissions
# TODO view owner missing permissions
