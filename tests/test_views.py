import csv
import json

import data_browser.models
import pytest
from data_browser import views
from data_browser.query import BoundQuery, Query
from django.contrib.auth.models import User

from . import models


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
    assert context.keys() == {"query", "data"}
    assert context["data"] == [[1, "a", "g"], [1, "b", "g"]]
    assert context["query"].keys() == {
        "model",
        "base_url",
        "csv_link",
        "save_link",
        "filters",
        "sort_fields",
        "all_fields_nested",
    }
    assert context["query"]["filters"] == [
        {
            "err_message": None,
            "is_valid": True,
            "lookup": "lt",
            "lookups": [
                {
                    "link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__equal=2",
                    "name": "equal",
                },
                {
                    "link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__not_equal=2",
                    "name": "not_equal",
                },
                {
                    "link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__gt=2",
                    "name": "gt",
                },
                {
                    "link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__gte=2",
                    "name": "gte",
                },
                {
                    "link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__lt=2",
                    "name": "lt",
                },
                {
                    "link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__lte=2",
                    "name": "lte",
                },
                {
                    "link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__is_null=2",
                    "name": "is_null",
                },
            ],
            "name": "size",
            "remove_link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0",
            "url_name": "size__lt",
            "value": 2.0,
        }
    ]

    assert context["query"]["sort_fields"] == [
        {
            "field": {
                "add_filter_link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__lt=2&size__equal=",
                "concrete": True,
                "name": "size",
                "remove_link": "/data_browser/query/tests/Product/+name,size_unit.html?id__gt=0&size__lt=2",
                "toggle_sort_link": "/data_browser/query/tests/Product/size,+name,size_unit.html?id__gt=0&size__lt=2",
            },
            "sort_icon": "\u2191",
        },
        {
            "field": {
                "add_filter_link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__lt=2&name__equals=",
                "concrete": True,
                "name": "name",
                "remove_link": "/data_browser/query/tests/Product/-size,size_unit.html?id__gt=0&size__lt=2",
                "toggle_sort_link": "/data_browser/query/tests/Product/-size,-name,size_unit.html?id__gt=0&size__lt=2",
            },
            "sort_icon": "\u2193",
        },
        {
            "field": {
                "add_filter_link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__lt=2&size_unit__equals=",
                "concrete": True,
                "name": "size_unit",
                "remove_link": "/data_browser/query/tests/Product/-size,+name.html?id__gt=0&size__lt=2",
                "toggle_sort_link": "/data_browser/query/tests/Product/-size,+name,+size_unit.html?id__gt=0&size__lt=2",
            },
            "sort_icon": "",
        },
    ]

    assert context["query"]["all_fields_nested"] == {
        "fields": [
            {
                "add_filter_link": "",
                "add_link": "/data_browser/query/tests/Product/-size,+name,size_unit,is_onsale.html?id__gt=0&size__lt=2",
                "concrete": False,
                "name": "is_onsale",
            },
            {
                "add_filter_link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__lt=2&name__equals=",
                "add_link": "/data_browser/query/tests/Product/-size,name,size_unit.html?id__gt=0&size__lt=2",
                "concrete": True,
                "name": "name",
            },
            {
                "add_filter_link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__lt=2&onsale__equal=",
                "add_link": "/data_browser/query/tests/Product/-size,+name,size_unit,onsale.html?id__gt=0&size__lt=2",
                "concrete": True,
                "name": "onsale",
            },
            {
                "add_filter_link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__lt=2&pk__equal=",
                "add_link": "/data_browser/query/tests/Product/-size,+name,size_unit,pk.html?id__gt=0&size__lt=2",
                "concrete": True,
                "name": "pk",
            },
            {
                "add_filter_link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__lt=2&size__equal=",
                "add_link": "/data_browser/query/tests/Product/size,+name,size_unit.html?id__gt=0&size__lt=2",
                "concrete": True,
                "name": "size",
            },
            {
                "add_filter_link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__lt=2&size_unit__equals=",
                "add_link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__lt=2",
                "concrete": True,
                "name": "size_unit",
            },
        ],
        "fks": [
            {
                "fields": [
                    {
                        "add_filter_link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__lt=2&default_sku__name__equals=",
                        "add_link": "/data_browser/query/tests/Product/-size,+name,size_unit,default_sku__name.html?id__gt=0&size__lt=2",
                        "concrete": True,
                        "name": "name",
                    }
                ],
                "fks": [],
                "name": "default_sku",
                "path": "default_sku",
            },
            {
                "fields": [],
                "fks": [],
                "name": "model_not_in_admin",
                "path": "model_not_in_admin",
            },
            {
                "fields": [
                    {
                        "add_filter_link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__lt=2&producer__name__equals=",
                        "add_link": "/data_browser/query/tests/Product/-size,+name,size_unit,producer__name.html?id__gt=0&size__lt=2",
                        "concrete": True,
                        "name": "name",
                    }
                ],
                "fks": [
                    {
                        "fields": [
                            {
                                "add_filter_link": "/data_browser/query/tests/Product/-size,+name,size_unit.html?id__gt=0&size__lt=2&producer__address__city__equals=",
                                "add_link": "/data_browser/query/tests/Product/-size,+name,size_unit,producer__address__city.html?id__gt=0&size__lt=2",
                                "concrete": True,
                                "name": "city",
                            }
                        ],
                        "fks": [],
                        "name": "address",
                        "path": "producer__address",
                    }
                ],
                "name": "producer",
                "path": "producer",
            },
        ],
    }


@pytest.mark.usefixtures("products")
def test_query_html_bad_fields(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests/Product/-size,+name,size_unit,-bob,is_onsale.html?size__lt=2&id__gt=0&bob__gt=1&size__xx=1&size__lt=xx"
    )
    assert res.status_code == 200
    assert json.loads(res.context["data"])["data"] == [
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
def test_view(admin_client):
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


# TODO calculated field, on admin, on model, both
# TODO missing permissions
# TODO view owner missing permissions
