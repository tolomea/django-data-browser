import csv

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
def get_query_data(fields):
    def helper(*args):
        query = Query.from_request(*args)
        bound_query = BoundQuery(query, fields)
        return views.get_data(bound_query)

    yield helper


@pytest.fixture
def get_product_data(get_query_data):
    return lambda *args, **kwargs: get_query_data("tests", "product", *args, **kwargs)


@pytest.mark.usefixtures("products")
def test_get_data_all(get_product_data):
    data = get_product_data("-size,+name,size_unit", "html", {})
    assert data == [[2, "c", "g"], [1, "a", "g"], [1, "b", "g"]]


@pytest.mark.usefixtures("products")
def test_get_empty(get_product_data):
    data = get_product_data("", "html", {})
    assert data == []


@pytest.mark.usefixtures("products")
def test_sort(get_product_data):
    data = get_product_data("+size,-name,size_unit", "html", {})
    assert data == [[1, "b", "g"], [1, "a", "g"], [2, "c", "g"]]


@pytest.mark.usefixtures("products")
def test_get_data_pks(get_product_data):
    data = get_product_data("pk", "html", {})
    assert {d[0] for d in data} == set(
        models.Product.objects.values_list("pk", flat=True)
    )


@pytest.mark.usefixtures("products")
def test_get_data_calculated_field(get_product_data):
    data = get_product_data("-size,+name,size_unit,is_onsale", "html", {})
    assert data == [[2, "c", "g", False], [1, "a", "g", False], [1, "b", "g", False]]


@pytest.mark.usefixtures("products")
def test_get_data_filtered(get_product_data):
    data = get_product_data("size,name", "html", {"name__equals": ["a"]})
    assert data == [[1, "a"]]


@pytest.mark.usefixtures("products")
def test_get_data_excluded(get_product_data):
    data = get_product_data("-size,name", "html", {"name__not_equals": ["a"]})
    assert data == [[2, "c"], [1, "b"]]


@pytest.mark.usefixtures("products")
def test_get_data_multi_excluded(get_product_data):
    data = get_product_data("-size,name", "html", {"name__not_equals": ["a", "c"]})
    assert data == [[1, "b"]]


@pytest.mark.usefixtures("products")
def test_get_data_collapsed(get_product_data):
    data = get_product_data("-size,size_unit", "html", {})
    assert data == [[2, "g"], [1, "g"]]


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
    assert res.context["data"] == [[1, "a", "g"], [1, "b", "g"]]


@pytest.mark.usefixtures("products")
def test_query_html_bad_fields(admin_client):
    res = admin_client.get(
        "/data_browser/query/tests/Product/-size,+name,size_unit,-bob.html?size__lt=2&id__gt=0&bob__gt=1&size__xx=1&size__lt=xx"
    )
    assert res.status_code == 200
    assert res.context["data"] == [[1, "a", "g"], [1, "b", "g"]]


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
def test_view_html(admin_client):
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


# calculated field, on admin, on model, both
# missing permissions
# view owner missing permissions
