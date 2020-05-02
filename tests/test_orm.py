import pytest
from data_browser import orm
from data_browser.query import BoundQuery, Query
from django.contrib.auth.models import Permission, User

from . import models


class ANY:  # pragma: no cover
    def __init__(self, type):
        self.type = type

    def __eq__(self, other):
        return isinstance(other, self.type)


class KEYS:  # pragma: no cover
    def __init__(self, *keys):
        self.keys = set(keys)

    def __eq__(self, other):
        return isinstance(other, dict) and other.keys() == self.keys


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
    return orm.get_all_model_fields(request)


@pytest.fixture
def get_query_data(all_model_fields, django_assert_num_queries):
    def helper(queries, *args):
        query = Query.from_request(*args)

        bound_query = BoundQuery(query, all_model_fields)
        with django_assert_num_queries(queries):
            return orm.get_data(bound_query)

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
def test_get_admin_field(get_product_data):
    data = get_product_data(1, "admin", {})
    assert data == [
        ['<a href="/admin/tests/product/1/change/">Product object (1)</a>'],
        ['<a href="/admin/tests/product/2/change/">Product object (2)</a>'],
        ['<a href="/admin/tests/product/3/change/">Product object (3)</a>'],
    ]


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
    data = get_product_data(1, "id", {})
    assert {d[0] for d in data} == set(
        models.Product.objects.values_list("id", flat=True)
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
    data = get_product_data(1, "id", {"onsale__is_null": ["True"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "id", {"onsale__is_null": ["true"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "id", {"onsale__is_null": ["False"]})
    assert data == []
    data = get_product_data(1, "id", {"onsale__is_null": ["false"]})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_data_boolean_filter(get_product_data):
    models.Product.objects.update(onsale=True)
    data = get_product_data(1, "id", {"onsale__equals": ["True"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "id", {"onsale__equals": ["true"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "id", {"onsale__equals": ["False"]})
    assert data == []
    data = get_product_data(1, "id", {"onsale__equals": ["false"]})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_data_string_filter(get_product_data):
    data = get_product_data(1, "id", {"producer__name__equals": ["Bob"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "id", {"producer__name__equals": ["bob"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "id", {"producer__name__equals": ["fred"]})
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

    # remap pk to id
    assert "pk" not in all_model_fields["tests.Product"]["fields"]
    assert "id" in all_model_fields["tests.Product"]["fields"]

    # no many to many fields
    assert "tags" not in all_model_fields["tests.Product"]["fields"]

    # no admin on inlines
    assert "admin" not in all_model_fields["tests.InlineAdmin"]["fields"]


class TestPermissions:
    def get_fields_with_perms(self, rf, perms):
        user = User.objects.create()
        for perm in perms:
            user.user_permissions.add(Permission.objects.get(codename=f"change_{perm}"))

        request = rf.get("/")
        request.user = user
        return orm.get_all_model_fields(request)

    def test_all_perms(self, rf, admin_user):
        all_model_fields = self.get_fields_with_perms(
            rf, ["normal", "notinadmin", "inadmin", "inlineadmin"]
        )

        assert "tests.NotInAdmin" not in all_model_fields
        assert all_model_fields["tests.InAdmin"] == {
            "fields": KEYS("admin", "id", "name"),
            "fks": {},
        }
        assert all_model_fields["tests.InlineAdmin"] == {
            "fields": KEYS("id", "name"),
            "fks": {"in_admin": "tests.InAdmin"},
        }
        assert all_model_fields["tests.Normal"] == {
            "fields": KEYS("admin", "id", "name"),
            "fks": {"in_admin": "tests.InAdmin", "inline_admin": "tests.InlineAdmin"},
        }

    @pytest.mark.django_db
    def test_no_perms(self, rf):
        all_model_fields = self.get_fields_with_perms(rf, ["normal"])

        assert "tests.NotInAdmin" not in all_model_fields
        assert "tests.InAdmin" not in all_model_fields
        assert "tests.InlineAdmin" not in all_model_fields
        assert all_model_fields["tests.Normal"] == {
            "fields": KEYS("admin", "id", "name"),
            "fks": {},
        }

    @pytest.mark.django_db
    def test_inline_perms(self, rf):
        all_model_fields = self.get_fields_with_perms(rf, ["normal", "inlineadmin"])

        assert "tests.NotInAdmin" not in all_model_fields
        assert "tests.InAdmin" not in all_model_fields
        assert "tests.InlineAdmin" not in all_model_fields
        assert all_model_fields["tests.Normal"] == {
            "fields": KEYS("admin", "id", "name"),
            "fks": {},
        }

    @pytest.mark.django_db
    def test_admin_perms(self, rf):
        all_model_fields = self.get_fields_with_perms(rf, ["normal", "inadmin"])

        assert "tests.NotInAdmin" not in all_model_fields
        assert all_model_fields["tests.InAdmin"] == {
            "fields": KEYS("admin", "id", "name"),
            "fks": {},
        }
        assert "tests.InlineAdmin" not in all_model_fields
        assert all_model_fields["tests.Normal"] == {
            "fields": KEYS("admin", "id", "name"),
            "fks": {"in_admin": "tests.InAdmin"},
        }
