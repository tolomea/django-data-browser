from datetime import datetime

import pytest
from data_browser import orm, orm_fields
from data_browser.query import BoundQuery, Query
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.auth.models import Permission, User
from django.utils import timezone

from . import models
from .util import ANY, KEYS


def flatten_table(fields, data):
    return [[row[f.path_str] for f in fields] for row in data]


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
def pivot_products(db):
    address = models.Address.objects.create(city="london", street="bad")
    producer = models.Producer.objects.create(name="Bob", address=address)
    datetimes = [
        datetime(2020, 1, 1),
        datetime(2020, 2, 1),
        datetime(2020, 2, 2),
        datetime(2021, 1, 1),
        datetime(2021, 1, 2),
        datetime(2021, 1, 3),
        datetime(2021, 2, 1),
        datetime(2021, 2, 2),
        datetime(2021, 2, 3),
        datetime(2021, 2, 4),
    ]
    for dt in datetimes:
        models.Product.objects.create(created_time=dt, name=str(dt), producer=producer)


@pytest.fixture
def req(rf, admin_user):
    req = rf.get("/")
    req.user = admin_user
    return req


@pytest.fixture
def orm_models(req):
    return orm.get_models(req)


@pytest.fixture
def get_product_flat(req, orm_models, django_assert_num_queries):
    def helper(queries, *args, **kwargs):
        query = Query.from_request("tests.Product", *args)
        bound_query = BoundQuery.bind(query, orm_models)
        with django_assert_num_queries(queries):
            data = orm.get_results(req, bound_query, orm_models)
            return flatten_table(bound_query.fields, data["rows"])

    return helper


@pytest.fixture
def get_product_pivot(req, orm_models, django_assert_num_queries):
    def helper(queries, *args, **kwargs):
        query = Query.from_request("tests.Product", *args)
        bound_query = BoundQuery.bind(query, orm_models)
        with django_assert_num_queries(queries):
            data = orm.get_results(req, bound_query, orm_models)
            return {
                "cols": flatten_table(bound_query.col_fields, data["cols"]),
                "rows": flatten_table(bound_query.row_fields, data["rows"]),
                "body": [
                    flatten_table(bound_query.data_fields, row) for row in data["body"]
                ],
            }

    return helper


@pytest.mark.usefixtures("products")
def test_get_results_all(get_product_flat):
    data = get_product_flat(1, "size-0,name+1,size_unit", {})
    assert data == [[2, "c", "g"], [1, "a", "g"], [1, "b", "g"]]


@pytest.mark.usefixtures("products")
def test_get_admin_link(get_product_flat):
    data = get_product_flat(2, "producer__address__admin", {})
    assert data == [
        [None],
        ['<a href="/admin/tests/address/1/change/">Address object (1)</a>'],
        ['<a href="/admin/tests/address/2/change/">Address object (2)</a>'],
    ]


@pytest.mark.usefixtures("products")
def test_get_calculated_field_on_admin(get_product_flat):
    data = get_product_flat(2, "producer__address__bob", {})
    assert data == [[None], ["bad"], ["bob"]]


@pytest.mark.usefixtures("products")
def test_get_multiple_calculated_fields_on_admins(get_product_flat):
    data = get_product_flat(3, "producer__address__bob,producer__frank", {})
    assert data == [[None, "frank"], ["bad", "frank"], ["bob", "frank"]]


@pytest.mark.usefixtures("products")
def test_get_calculated_field(get_product_flat):
    data = get_product_flat(2, "producer__address__fred", {})
    assert data == [[None], ["bad"], ["fred"]]


@pytest.mark.usefixtures("products")
def test_get_property(get_product_flat):
    data = get_product_flat(2, "producer__address__tom", {})
    assert data == [[None], ["bad"], ["tom"]]


@pytest.mark.usefixtures("products")
def test_get_time_function(get_product_flat):
    data = get_product_flat(1, "created_time__year", {})
    assert data == [[timezone.now().year]]


@pytest.mark.usefixtures("products")
def test_get_aggregate(get_product_flat):
    data = get_product_flat(1, "size_unit,id__count", {})
    assert data == [["g", 3]]


@pytest.mark.usefixtures("products")
def test_get_time_aggregate(get_product_flat):
    data = get_product_flat(1, "size_unit,created_time__count", {})
    assert data == [["g", 1]]


@pytest.mark.usefixtures("products")
def test_filter_and_get_aggregate(get_product_flat):
    data = get_product_flat(1, "size_unit,id__count", {"id__count__gt": [0]})
    assert data == [["g", 3]]


@pytest.mark.usefixtures("products")
def test_filter_aggregate(get_product_flat):
    data = get_product_flat(1, "size_unit", {"id__count__gt": [0]})
    assert data == [["g"]]


@pytest.mark.usefixtures("products")
def test_get_aggregate_and_calculated_field(get_product_flat):
    data = get_product_flat(2, "is_onsale,id__count", {})
    assert data == [[False, 1], [False, 1], [False, 1]]


@pytest.mark.usefixtures("products")
def test_get_time_aggregate_and_calculated_field(get_product_flat):
    data = get_product_flat(2, "is_onsale,created_time__count", {})
    assert data == [[False, 1], [False, 1], [False, 1]]


@pytest.mark.usefixtures("products")
def test_get_only_aggregate(get_product_flat):
    data = get_product_flat(1, "id__count", {})
    assert data == [[3]]


@pytest.mark.usefixtures("products")
def test_get_results_empty(get_product_flat):
    data = get_product_flat(0, "", {})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_results_sort(get_product_flat):
    data = get_product_flat(1, "size+0,name-1,size_unit", {})
    assert data == [[1, "b", "g"], [1, "a", "g"], [2, "c", "g"]]


@pytest.mark.usefixtures("products")
def test_get_results_pks(get_product_flat):
    data = get_product_flat(1, "id", {})
    assert {d[0] for d in data} == set(
        models.Product.objects.values_list("id", flat=True)
    )


@pytest.mark.usefixtures("products")
def test_get_results_calculated_field(get_product_flat):
    # query + prefetch producer
    data = get_product_flat(2, "name+0,producer__name,is_onsale", {})
    assert data == [["a", "Bob", False], ["b", "Bob", False], ["c", "Bob", False]]


@pytest.mark.usefixtures("products")
def test_get_results_filtered(get_product_flat):
    data = get_product_flat(1, "size,name", {"name__equals": ["a"]})
    assert data == [[1, "a"]]


@pytest.mark.usefixtures("products")
def test_get_results_excluded(get_product_flat):
    data = get_product_flat(1, "size-0,name", {"name__not_equals": ["a"]})
    assert data == [[2, "c"], [1, "b"]]


@pytest.mark.usefixtures("products")
def test_get_results_multi_excluded(get_product_flat):
    data = get_product_flat(1, "size-0,name", {"name__not_equals": ["a", "c"]})
    assert data == [[1, "b"]]


@pytest.mark.usefixtures("products")
def test_get_results_collapsed(get_product_flat):
    data = get_product_flat(1, "size-0,size_unit", {})
    assert data == [[2, "g"], [1, "g"]]


@pytest.mark.usefixtures("products")
def test_get_results_null_filter(get_product_flat):
    data = get_product_flat(1, "id", {"onsale__is_null": ["True"]})
    assert data == [[1], [2], [3]]
    data = get_product_flat(1, "id", {"onsale__is_null": ["true"]})
    assert data == [[1], [2], [3]]
    data = get_product_flat(1, "id", {"onsale__is_null": ["False"]})
    assert data == []
    data = get_product_flat(1, "id", {"onsale__is_null": ["false"]})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_results_boolean_filter(get_product_flat):
    models.Product.objects.update(onsale=True)
    data = get_product_flat(1, "id", {"onsale__equals": ["True"]})
    assert data == [[1], [2], [3]]
    data = get_product_flat(1, "id", {"onsale__equals": ["true"]})
    assert data == [[1], [2], [3]]
    data = get_product_flat(1, "id", {"onsale__equals": ["False"]})
    assert data == []
    data = get_product_flat(1, "id", {"onsale__equals": ["false"]})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_results_string_filter(get_product_flat):
    data = get_product_flat(1, "id", {"producer__name__equals": ["Bob"]})
    assert data == [[1], [2], [3]]
    data = get_product_flat(1, "id", {"producer__name__equals": ["bob"]})
    assert data == [[1], [2], [3]]
    data = get_product_flat(1, "id", {"producer__name__equals": ["fred"]})
    assert data == []


@pytest.mark.usefixtures("products")
def test_get_results_basic_flat(get_product_flat):
    # just a query
    data = get_product_flat(1, "name+0,producer__address__city", {})
    assert data == [["a", "london"], ["b", "london"], ["c", None]]


@pytest.mark.usefixtures("products")
def test_get_results_calculated_causes_query(get_product_flat):
    # query products, fetch objects for calculated
    data = get_product_flat(2, "name+0,is_onsale,producer__address__city", {})
    assert data == [["a", False, "london"], ["b", False, "london"], ["c", False, None]]


@pytest.mark.usefixtures("products")
def test_get_results_admin_causes_query(get_product_flat):
    # query products, fetch objects for calculated
    data = get_product_flat(2, "name+0,admin,producer__address__city", {})
    assert data == [
        [
            "a",
            '<a href="/admin/tests/product/1/change/">Product object (1)</a>',
            "london",
        ],
        [
            "b",
            '<a href="/admin/tests/product/2/change/">Product object (2)</a>',
            "london",
        ],
        ["c", '<a href="/admin/tests/product/3/change/">Product object (3)</a>', None],
    ]


@pytest.mark.usefixtures("pivot_products")
def test_get_pivot(get_product_pivot):
    data = get_product_pivot(3, "created_time__year,&created_time__month,id__count", {})
    assert data == {
        "body": [[[1], [3]], [[2], [4]]],
        "cols": [["January"], ["Feburary"]],
        "rows": [[2020], [2021]],
    }


@pytest.mark.usefixtures("pivot_products")
def test_get_pivot_multi_agg(get_product_pivot):
    data = get_product_pivot(
        3, "created_time__year,&created_time__month,id__count,id__max", {}
    )
    assert data == {
        "body": [[[1, 1], [3, 6]], [[2, 3], [4, 10]]],
        "cols": [["January"], ["Feburary"]],
        "rows": [[2020], [2021]],
    }


@pytest.mark.usefixtures("pivot_products")
def test_get_pivot_all(get_product_pivot):
    data = get_product_pivot(
        1, "&created_time__year, &created_time__month,id__count", {}
    )
    assert data == {
        "body": [[[1]], [[2]], [[3]], [[4]]],
        "cols": [
            [2020, "January"],
            [2020, "Feburary"],
            [2021, "January"],
            [2021, "Feburary"],
        ],
        "rows": [[]],
    }


def test_pivot_sorting(get_product_pivot):
    address = models.Address.objects.create(city="london", street="bad")
    producer = models.Producer.objects.create(name="Bob", address=address)
    datetimes = [
        # 2021, 1, 1 is notably missing
        datetime(2021, 2, 1),
        datetime(2022, 1, 1),
        datetime(2022, 1, 2),
        datetime(2022, 2, 1),
        datetime(2022, 2, 2),
        datetime(2022, 2, 3),
    ]
    for dt in datetimes:
        models.Product.objects.create(created_time=dt, name=str(dt), producer=producer)

    data = get_product_pivot(
        3, "&created_time__year+1,created_time__month+2,id__count", {}
    )
    assert data == {
        "body": [[[None], [1]], [[2], [3]]],
        "rows": [["January"], ["Feburary"]],
        "cols": [[2021], [2022]],
    }

    data = get_product_pivot(
        3, "&created_time__year+2,created_time__month+1,id__count", {}
    )
    assert data == {
        "body": [[[None], [1]], [[2], [3]]],
        "rows": [["January"], ["Feburary"]],
        "cols": [[2021], [2022]],
    }


@pytest.mark.usefixtures("pivot_products")
def test_pivot_having(get_product_pivot):
    data = get_product_pivot(
        3,
        "&created_time__year,created_time__month,id__count",
        {"id__count__equals": [4]},
    )
    assert data == {"body": [[[4]]], "rows": [["Feburary"]], "cols": [[2021]]}


jan = "January"
feb = "Feburary"
testdata = [
    ("----", [], [], []),
    ("---b", [[0, None]], [[]], [[[]]]),
    ("--c-", [], [], []),
    ("--cb", [], [], []),
    ("-r--", [], [], []),
    ("-r-b", [], [], []),
    ("-rc-", [], [], []),
    ("-rcb", [], [], []),
    ("d---", [], [], []),
    ("d--b", [[10, 10]], [[]], [[[]]]),
    ("d-c-", [[]], [[jan], [feb]], [[[]], [[]]]),
    ("d-cb", [[]], [[jan], [feb]], [[[4, 6]], [[6, 10]]]),
    ("dr--", [[2020], [2021]], [[]], [[[], []]]),
    ("dr-b", [[2020, 3, 3], [2021, 7, 10]], [[]], [[[], []]]),
    ("drc-", [[2020], [2021]], [[jan], [feb]], [[[], []], [[], []]]),
    ("drcb", [[2020], [2021]], [[jan], [feb]], [[[1, 1], [3, 6]], [[2, 3], [4, 10]]]),
]


@pytest.mark.usefixtures("pivot_products")
@pytest.mark.parametrize("key,rows,cols,body", testdata)
def test_get_pivot_permutations(get_product_pivot, key, rows, cols, body):
    fields = []
    if "r" in key:
        fields.append("created_time__year")
    if "c" in key:
        fields.append("&created_time__month")
    if "b" in key:
        fields.extend(["id__count", "id__max"])
    filters = {} if "d" in key else {"id__equals": ["123"]}

    queries = 0 if key.endswith("---") else 1
    if "r" in key and "c" in key:
        queries += 2

    results = get_product_pivot(queries, ",".join(fields), filters)
    assert results["rows"] == rows
    assert results["cols"] == cols
    assert results["body"] == body


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
        assert orm_models["tests.InAdmin"] == orm_fields.OrmModel(
            fields=KEYS("admin", "id", "name"), admin=ANY(BaseModelAdmin)
        )
        assert orm_models["tests.InlineAdmin"] == orm_fields.OrmModel(
            fields=KEYS("id", "name", "in_admin"), admin=ANY(BaseModelAdmin)
        )
        assert orm_models["tests.Normal"] == orm_fields.OrmModel(
            fields=KEYS("admin", "id", "name", "in_admin", "inline_admin"),
            admin=ANY(BaseModelAdmin),
        )

    @pytest.mark.django_db
    def test_no_perms(self, rf):
        orm_models = self.get_fields_with_perms(rf, ["normal"])

        assert "tests.NotInAdmin" not in orm_models
        assert "tests.InAdmin" not in orm_models
        assert "tests.InlineAdmin" not in orm_models
        assert orm_models["tests.Normal"] == orm_fields.OrmModel(
            fields=KEYS("admin", "id", "name"), admin=ANY(BaseModelAdmin)
        )

    @pytest.mark.django_db
    def test_inline_perms(self, rf):
        orm_models = self.get_fields_with_perms(rf, ["normal", "inlineadmin"])

        assert "tests.NotInAdmin" not in orm_models
        assert "tests.InAdmin" not in orm_models
        assert "tests.InlineAdmin" not in orm_models
        assert orm_models["tests.Normal"] == orm_fields.OrmModel(
            fields=KEYS("admin", "id", "name"), admin=ANY(BaseModelAdmin)
        )

    @pytest.mark.django_db
    def test_admin_perms(self, rf):
        orm_models = self.get_fields_with_perms(rf, ["normal", "inadmin"])

        assert "tests.NotInAdmin" not in orm_models
        assert orm_models["tests.InAdmin"] == orm_fields.OrmModel(
            fields=KEYS("admin", "id", "name"), admin=ANY(BaseModelAdmin)
        )
        assert "tests.InlineAdmin" not in orm_models
        assert orm_models["tests.Normal"] == orm_fields.OrmModel(
            fields=KEYS("admin", "id", "name", "in_admin"), admin=ANY(BaseModelAdmin)
        )
