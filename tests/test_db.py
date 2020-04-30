import pytest
from data_browser import db
from data_browser.query import BoundQuery, Query

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
def all_model_fields(rf, admin_user):
    request = rf.get("/")
    request.user = admin_user
    return db.get_all_model_fields(request)


@pytest.fixture
def get_query_data(all_model_fields, django_assert_num_queries):
    def helper(queries, *args):
        query = Query.from_request(*args)

        bound_query = BoundQuery(query, all_model_fields)
        with django_assert_num_queries(queries):
            return db.get_data(bound_query)

    yield helper


@pytest.fixture
def get_product_data(get_query_data):
    return lambda queries, *args, **kwargs: get_query_data(
        queries, "tests.Product", *args, **kwargs
    )


@pytest.mark.usefixtures("products")
def test_get_data_all(get_product_data):
    data = get_product_data(1, "-size,+name,size_unit", {})
    assert data == [[2, "c", "g"], [1, "a", "g"], [1, "b", "g"]]


@pytest.mark.usefixtures("products")
def test_get_data_empty(get_product_data):
    data = get_product_data(0, "", {})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_data_sort(get_product_data):
    data = get_product_data(1, "+size,-name,size_unit", {})
    assert data == [[1, "b", "g"], [1, "a", "g"], [2, "c", "g"]]


@pytest.mark.usefixtures("products")
def test_get_data_pks(get_product_data):
    data = get_product_data(1, "pk", {})
    assert {d[0] for d in data} == set(
        models.Product.objects.values_list("pk", flat=True)
    )


@pytest.mark.usefixtures("products")
def test_get_data_calculated_field(get_product_data):
    # query + prefetch producer
    data = get_product_data(2, "+name,producer__name,is_onsale", {})
    assert data == [["a", "Bob", False], ["b", "Bob", False], ["c", "Bob", False]]


@pytest.mark.usefixtures("products")
def test_get_data_filtered(get_product_data):
    data = get_product_data(1, "size,name", {"name__equals": ["a"]})
    assert data == [[1, "a"]]


@pytest.mark.usefixtures("products")
def test_get_data_excluded(get_product_data):
    data = get_product_data(1, "-size,name", {"name__not_equals": ["a"]})
    assert data == [[2, "c"], [1, "b"]]


@pytest.mark.usefixtures("products")
def test_get_data_multi_excluded(get_product_data):
    data = get_product_data(1, "-size,name", {"name__not_equals": ["a", "c"]})
    assert data == [[1, "b"]]


@pytest.mark.usefixtures("products")
def test_get_data_collapsed(get_product_data):
    data = get_product_data(1, "-size,size_unit", {})
    assert data == [[2, "g"], [1, "g"]]


@pytest.mark.usefixtures("products")
def test_get_data_null_filter(get_product_data):
    data = get_product_data(1, "pk", {"onsale__is_null": ["True"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "pk", {"onsale__is_null": ["true"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "pk", {"onsale__is_null": ["False"]})
    assert data == []
    data = get_product_data(1, "pk", {"onsale__is_null": ["false"]})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_data_boolean_filter(get_product_data):
    models.Product.objects.update(onsale=True)
    data = get_product_data(1, "pk", {"onsale__equals": ["True"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "pk", {"onsale__equals": ["true"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "pk", {"onsale__equals": ["False"]})
    assert data == []
    data = get_product_data(1, "pk", {"onsale__equals": ["false"]})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_data_string_filter(get_product_data):
    data = get_product_data(1, "pk", {"producer__name__equals": ["Bob"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "pk", {"producer__name__equals": ["bob"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "pk", {"producer__name__equals": ["fred"]})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_data_prefetch(get_product_data):
    # query products, prefetch producer, producer__address
    data = get_product_data(3, "+name,is_onsale,producer__address__city", {})
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
    data = get_product_data(1, "+name,producer__address__city", {})
    assert data == [["a", "london"], ["b", "london"], ["c", "london"]]


@pytest.mark.usefixtures("products")
def test_get_data_sort_causes_select(get_product_data):
    # query products, join the rest
    data = get_product_data(1, "+name,is_onsale,-producer__address__city", {})
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
        {"producer__address__city__equals": ["london"]},
    )
    assert data == [
        ["a", False, "london"],
        ["b", False, "london"],
        ["c", False, "london"],
    ]


def test_get_fields(all_model_fields):
    # basic
    assert "name" in all_model_fields["tests.Product"]["fields"]

    # remap id to pk
    assert "id" not in all_model_fields["tests.Product"]["fields"]
    assert "pk" in all_model_fields["tests.Product"]["fields"]

    # follow fk
    assert "producer" not in all_model_fields["tests.Product"]["fields"]
    assert "producer" in all_model_fields["tests.Product"]["fks"]
    assert "name" in all_model_fields["tests.Producer"]["fields"]

    # follow multiple fk's
    assert "city" in all_model_fields["tests.Address"]["fields"]

    # no many to many fields
    assert "tags" not in all_model_fields["tests.Product"]["fields"]

    # check in and out of admin
    assert "not_in_admin" not in all_model_fields["tests.Product"]["fields"]
    assert "fk_not_in_admin" not in all_model_fields["tests.Product"]["fks"]
    assert "model_not_in_admin" in all_model_fields["tests.Product"]["fks"]
    assert "tests.NotInAdmin" not in all_model_fields
