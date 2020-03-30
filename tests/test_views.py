import pytest
from data_browser import views
from data_browser.query import BoundQuery, Query

from . import models


@pytest.fixture
def products(db):
    producer = models.Producer.objects.create(name="bob")
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


@pytest.mark.usefixtures("products")
def test_get_data_all(get_query_data):
    data = get_query_data("tests", "product", "-size,+name,size_unit", "html", {})
    assert data == [[2, "c", "g"], [1, "a", "g"], [1, "b", "g"]]


@pytest.mark.usefixtures("products")
def test_get_empty(get_query_data):
    data = get_query_data("tests", "product", "", "html", {})
    assert data == []


@pytest.mark.usefixtures("products")
def test_sort(get_query_data):
    data = get_query_data("tests", "product", "+size,-name,size_unit", "html", {})
    assert data == [[1, "b", "g"], [1, "a", "g"], [2, "c", "g"]]


@pytest.mark.usefixtures("products")
def test_get_data_pks(get_query_data):
    data = get_query_data("tests", "product", "pk", "html", {})
    assert {d[0] for d in data} == set(
        models.Product.objects.values_list("pk", flat=True)
    )


@pytest.mark.usefixtures("products")
def test_get_data_calculated_field(get_query_data):
    data = get_query_data(
        "tests", "product", "-size,+name,size_unit,is_onsale", "html", {}
    )
    assert data == [[2, "c", "g", False], [1, "a", "g", False], [1, "b", "g", False]]


@pytest.mark.usefixtures("products")
def test_get_data_filtered(get_query_data):
    data = get_query_data(
        "tests", "product", "size,name", "html", {"name__equals": ["a"]}
    )
    assert data == [[1, "a"]]


@pytest.mark.usefixtures("products")
def test_get_data_excluded(get_query_data):
    data = get_query_data(
        "tests", "product", "-size,name", "html", {"name__not_equals": ["a"]}
    )
    assert data == [[2, "c"], [1, "b"]]


@pytest.mark.usefixtures("products")
def test_get_data_multi_excluded(get_query_data):
    data = get_query_data(
        "tests", "product", "-size,name", "html", {"name__not_equals": ["a", "c"]}
    )
    assert data == [[1, "b"]]


@pytest.mark.usefixtures("products")
def test_get_data_collapsed(get_query_data):
    data = get_query_data("tests", "product", "-size,size_unit", "html", {})
    assert data == [[2, "g"], [1, "g"]]


def test_get_fields(fields):
    fields, groups = fields

    # basic
    assert "name" in fields

    # remap id to pk
    assert "id" not in fields
    assert "pk" in fields

    # recurse
    assert "producer" not in fields
    assert "producer" in groups
    assert "name" in groups["producer"][0]


# no loops
# assert "product" not in groups["default_sku"][1]

# multi recursion
# assert "name" in groups["producer"][1]["shipping_address"][0]

# fk - field in admin model not, model in admin field not
# fields not in admin
# calculated field, on admin, on model, both, on model with arg
