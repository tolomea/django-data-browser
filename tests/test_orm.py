import pytest
from data_browser import orm
from data_browser.query import BoundQuery, NumberFieldType, Query, StringFieldType
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.auth.models import Permission, User
from django.utils import timezone

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
    now = timezone.now()

    address = models.Address.objects.create(city="london", street="bad")
    producer = models.Producer.objects.create(name="Bob", address=address)
    models.Product.objects.create(
        created_time=now, name="a", size=1, size_unit="g", producer=producer
    )

    address = models.Address.objects.create(city="london", street="good")
    producer = models.Producer.objects.create(name="Bob", address=address)
    models.Product.objects.create(
        created_time=now, name="b", size=1, size_unit="g", producer=producer
    )

    producer = models.Producer.objects.create(name="Bob", address=None)
    models.Product.objects.create(
        created_time=now, name="c", size=2, size_unit="g", producer=producer
    )


@pytest.fixture
def req(rf, admin_user):
    req = rf.get("/")
    req.user = admin_user
    return req


@pytest.fixture
def orm_models(req):
    return orm.get_models(req)


@pytest.fixture
def get_query_data(req, orm_models, django_assert_num_queries):
    def helper(queries, *args):
        query = Query.from_request(*args)

        bound_query = BoundQuery(query, orm_models)
        with django_assert_num_queries(queries):
            return orm.get_results(req, bound_query)

    yield helper


@pytest.fixture
def get_product_data(get_query_data):
    return lambda queries, *args, **kwargs: get_query_data(
        queries, "tests.Product", *args, **kwargs
    )


@pytest.mark.usefixtures("products")
def test_get_results_all(get_product_data):
    data = get_product_data(1, "size-0,name+1,size_unit", {})
    assert data == [[2, "c", "g"], [1, "a", "g"], [1, "b", "g"]]


@pytest.mark.usefixtures("products")
def test_get_admin_link(get_product_data):
    data = get_product_data(3, "producer__address__admin", {})
    assert data == [
        ['<a href="/admin/tests/address/1/change/">Address object (1)</a>'],
        ['<a href="/admin/tests/address/2/change/">Address object (2)</a>'],
        [None],
    ]


@pytest.mark.usefixtures("products")
def test_get_admin_function(get_product_data):
    data = get_product_data(3, "producer__address__bob", {})
    assert data == [["bad"], ["bob"], [None]]


@pytest.mark.usefixtures("products")
def test_get_function(get_product_data):
    data = get_product_data(3, "producer__address__fred", {})
    assert data == [["bad"], ["fred"], [None]]


@pytest.mark.usefixtures("products")
def test_get_property(get_product_data):
    data = get_product_data(3, "producer__address__tom", {})
    assert data == [["bad"], ["tom"], [None]]


@pytest.mark.usefixtures("products")
def test_get_aggregate(get_product_data):
    data = get_product_data(1, "size_unit,id__count", {})
    assert data == [["g", 3]]


@pytest.mark.usefixtures("products")
def test_get_time_aggregate(get_product_data):
    data = get_product_data(1, "size_unit,created_time__count", {})
    assert data == [["g", 1]]


@pytest.mark.usefixtures("products")
def test_filter_and_get_aggregate(get_product_data):
    data = get_product_data(1, "size_unit,id__count", {"id__count__gt": [0]})
    assert data == [["g", 3]]


@pytest.mark.usefixtures("products")
def test_filter_aggregate(get_product_data):
    data = get_product_data(1, "size_unit", {"id__count__gt": [0]})
    assert data == [["g"]]


@pytest.mark.usefixtures("products")
def test_get_aggregate_and_function(get_product_data):
    data = get_product_data(1, "is_onsale,id__count", {})
    assert data == [[False, 1], [False, 1], [False, 1]]


@pytest.mark.usefixtures("products")
def test_get_time_aggregate_and_function(get_product_data):
    data = get_product_data(1, "is_onsale,created_time__count", {})
    assert data == [[False, 1], [False, 1], [False, 1]]


@pytest.mark.usefixtures("products")
def test_get_only_aggregate(get_product_data):
    data = get_product_data(1, "id__count", {})
    assert data == [[3]]


@pytest.mark.usefixtures("products")
def test_get_results_empty(get_product_data):
    data = get_product_data(0, "", {})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_results_sort(get_product_data):
    data = get_product_data(1, "size+0,name-1,size_unit", {})
    assert data == [[1, "b", "g"], [1, "a", "g"], [2, "c", "g"]]


@pytest.mark.usefixtures("products")
def test_get_results_pks(get_product_data):
    data = get_product_data(1, "id", {})
    assert {d[0] for d in data} == set(
        models.Product.objects.values_list("id", flat=True)
    )


@pytest.mark.usefixtures("products")
def test_get_results_calculated_field(get_product_data):
    # query + prefetch producer
    data = get_product_data(2, "name+0,producer__name,is_onsale", {})
    assert data == [["a", "Bob", False], ["b", "Bob", False], ["c", "Bob", False]]


@pytest.mark.usefixtures("products")
def test_get_results_filtered(get_product_data):
    data = get_product_data(1, "size,name", {"name__equals": ["a"]})
    assert data == [[1, "a"]]


@pytest.mark.usefixtures("products")
def test_get_results_excluded(get_product_data):
    data = get_product_data(1, "size-0,name", {"name__not_equals": ["a"]})
    assert data == [[2, "c"], [1, "b"]]


@pytest.mark.usefixtures("products")
def test_get_results_multi_excluded(get_product_data):
    data = get_product_data(1, "size-0,name", {"name__not_equals": ["a", "c"]})
    assert data == [[1, "b"]]


@pytest.mark.usefixtures("products")
def test_get_results_collapsed(get_product_data):
    data = get_product_data(1, "size-0,size_unit", {})
    assert data == [[2, "g"], [1, "g"]]


@pytest.mark.usefixtures("products")
def test_get_results_null_filter(get_product_data):
    data = get_product_data(1, "id", {"onsale__is_null": ["True"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "id", {"onsale__is_null": ["true"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "id", {"onsale__is_null": ["False"]})
    assert data == []
    data = get_product_data(1, "id", {"onsale__is_null": ["false"]})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_results_boolean_filter(get_product_data):
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
def test_get_results_string_filter(get_product_data):
    data = get_product_data(1, "id", {"producer__name__equals": ["Bob"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "id", {"producer__name__equals": ["bob"]})
    assert data == [[1], [2], [3]]
    data = get_product_data(1, "id", {"producer__name__equals": ["fred"]})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_results_prefetch(get_product_data):
    # query products, prefetch producer, producer__address
    data = get_product_data(3, "name+0,is_onsale,producer__address__city", {})
    assert data == [["a", False, "london"], ["b", False, "london"], ["c", False, None]]


@pytest.mark.usefixtures("products")
def test_get_results_prefetch_with_filter(get_product_data):
    # query products, join to producer, producer__address
    data = get_product_data(
        1,
        "name+0,is_onsale,producer__address__city",
        {"producer__address__city__not_equals": ["Invercargill"]},
    )
    assert data == [["a", False, "london"], ["b", False, "london"], ["c", False, None]]


@pytest.mark.usefixtures("products")
def test_get_results_no_calculated_so_flat(get_product_data):
    # query products, join the rest
    data = get_product_data(1, "name+0,producer__address__city", {})
    assert data == [["a", "london"], ["b", "london"], ["c", None]]


@pytest.mark.usefixtures("products")
def test_get_results_sort_causes_select(get_product_data):
    # query products, join the rest
    data = get_product_data(1, "name+0,is_onsale,producer__address__city-1", {})
    assert data == [["a", False, "london"], ["b", False, "london"], ["c", False, None]]


@pytest.mark.usefixtures("products")
def test_get_results_filter_causes_select(get_product_data):
    # query products, join the rest
    data = get_product_data(
        1,
        "name+0,is_onsale,producer__address__city",
        {"producer__address__city__equals": ["london"]},
    )
    assert data == [["a", False, "london"], ["b", False, "london"]]


def test_get_fields(orm_models):

    # remap pk to id
    assert "pk" not in orm_models["tests.Product"].fields
    assert "id" in orm_models["tests.Product"].fields

    # no many to many fields
    assert "tags" not in orm_models["tests.Product"].fields

    # no admin on inlines
    assert "admin" not in orm_models["tests.InlineAdmin"].fields


class TestPermissions:
    def get_fields_with_perms(self, rf, perms):
        user = User.objects.create()
        for perm in perms:
            user.user_permissions.add(Permission.objects.get(codename=f"change_{perm}"))

        request = rf.get("/")
        request.user = user
        return orm.get_models(request)

    def test_all_perms(self, rf, admin_user):
        orm_models = self.get_fields_with_perms(
            rf, ["normal", "notinadmin", "inadmin", "inlineadmin"]
        )

        assert "tests.NotInAdmin" not in orm_models
        assert orm_models["tests.InAdmin"] == orm.OrmModel(
            fields=KEYS("admin", "id", "name"), admin=ANY(BaseModelAdmin)
        )
        assert orm_models["tests.InlineAdmin"] == orm.OrmModel(
            fields=KEYS("id", "name", "in_admin"), admin=ANY(BaseModelAdmin)
        )
        assert orm_models["tests.Normal"] == orm.OrmModel(
            fields=KEYS("admin", "id", "name", "in_admin", "inline_admin"),
            admin=ANY(BaseModelAdmin),
        )

    @pytest.mark.django_db
    def test_no_perms(self, rf):
        orm_models = self.get_fields_with_perms(rf, ["normal"])

        assert "tests.NotInAdmin" not in orm_models
        assert "tests.InAdmin" not in orm_models
        assert "tests.InlineAdmin" not in orm_models
        assert orm_models["tests.Normal"] == orm.OrmModel(
            fields=KEYS("admin", "id", "name"), admin=ANY(BaseModelAdmin)
        )

    @pytest.mark.django_db
    def test_inline_perms(self, rf):
        orm_models = self.get_fields_with_perms(rf, ["normal", "inlineadmin"])

        assert "tests.NotInAdmin" not in orm_models
        assert "tests.InAdmin" not in orm_models
        assert "tests.InlineAdmin" not in orm_models
        assert orm_models["tests.Normal"] == orm.OrmModel(
            fields=KEYS("admin", "id", "name"), admin=ANY(BaseModelAdmin)
        )

    @pytest.mark.django_db
    def test_admin_perms(self, rf):
        orm_models = self.get_fields_with_perms(rf, ["normal", "inadmin"])

        assert "tests.NotInAdmin" not in orm_models
        assert orm_models["tests.InAdmin"] == orm.OrmModel(
            fields=KEYS("admin", "id", "name"), admin=ANY(BaseModelAdmin)
        )
        assert "tests.InlineAdmin" not in orm_models
        assert orm_models["tests.Normal"] == orm.OrmModel(
            fields=KEYS("admin", "id", "name", "in_admin"), admin=ANY(BaseModelAdmin)
        )


def test_path_properties():
    db_field = orm.OrmConcreteField("", "joe", "joe", StringFieldType)
    orm_field = orm.OrmConcreteField("string", "max", "max", NumberFieldType)

    bf = orm.OrmBoundField(
        orm_field, db_field, ["bob", "fred"], ["bob", "fred", "joe", "max"]
    )
    assert bf.field_path_str == "bob__fred__joe"
    assert bf.full_path_str == "bob__fred__joe__max"

    bf = orm.OrmBoundField(orm_field, db_field, [], ["joe", "max"])

    assert bf.field_path_str == "joe"
    assert bf.full_path_str == "joe__max"

    bf = orm.OrmBoundField(db_field, db_field, ["bob", "fred"], ["bob", "fred", "joe"])

    assert bf.field_path_str == "bob__fred__joe"
    assert bf.full_path_str == "bob__fred__joe"
