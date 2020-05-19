from datetime import datetime

import pytest
from data_browser import orm
from data_browser.query import (
    ASC,
    DSC,
    BooleanFieldType,
    BoundField,
    BoundFilter,
    BoundQuery,
    NumberFieldType,
    Query,
    QueryField,
    QueryFilter,
    StringFieldType,
    TimeFieldType,
)
from django.utils import timezone


@pytest.fixture
def query():
    return Query(
        "app.model",
        [QueryField("fa", ASC, 1), QueryField("fd", DSC, 0), QueryField("fn")],
        [QueryFilter("bob", "equals", "fred")],
    )


@pytest.fixture
def orm_models():
    return {
        "app.model": orm.OrmModel(
            fields={
                "fa": orm.OrmField(
                    type_=StringFieldType, concrete=True, model_name="app.model"
                ),
                "fd": orm.OrmField(
                    type_=StringFieldType, concrete=True, model_name="app.model"
                ),
                "fn": orm.OrmField(
                    type_=StringFieldType, concrete=False, model_name="app.model"
                ),
                "bob": orm.OrmField(
                    type_=StringFieldType, concrete=True, model_name="app.model"
                ),
                "num": orm.OrmField(
                    type_=NumberFieldType, concrete=True, model_name="app.model"
                ),
            },
            fks={"tom": orm.OrmFkField("app.Tom")},
        ),
        "app.Tom": orm.OrmModel(
            fields={
                "jones": orm.OrmField(
                    type_=StringFieldType, concrete=True, model_name="app.Tom"
                )
            },
            fks={"michael": orm.OrmFkField("app.Michael")},
        ),
        "app.Michael": orm.OrmModel(
            fields={
                "bolton": orm.OrmField(
                    type_=StringFieldType, concrete=True, model_name="app.Michael"
                )
            },
            fks={},
        ),
    }


@pytest.fixture
def bound_query(query, orm_models):
    return BoundQuery(query, orm_models)


@pytest.fixture
def fake_orm_field():
    class FakeOrmField:
        type_ = StringFieldType
        concrete = False

    return FakeOrmField()


class TestQuery:
    def test_from_request(self, query):
        q = Query.from_request("app.model", "fa+1,fd-0,fn", {"bob__equals": ["fred"]})
        assert q == query

    def test_from_request_with_related_filter(self):
        q = Query.from_request(
            "app.model", "fa+1,fd-0,fn", {"bob__jones__equals": ["fred"]}
        )
        assert q == Query(
            "app.model",
            [QueryField("fa", ASC, 1), QueryField("fd", DSC, 0), QueryField("fn")],
            [QueryFilter("bob__jones", "equals", "fred")],
        )

    def test_from_request_with_missing(self, query):
        q = Query.from_request("app.model", "fa+1,,fd-0,fn", {"bob__equals": ["fred"]})
        assert q == query

    def test_url(self, query):
        assert (
            query.get_url("html")
            == "/data_browser/query/app.model/fa+1,fd-0,fn.html?bob__equals=fred"
        )

    def test_url_no_filters(self, query):
        query.filters = []
        assert (
            query.get_url("html") == "/data_browser/query/app.model/fa+1,fd-0,fn.html?"
        )


class TestBoundQuery:
    def test_fields(self, bound_query):
        assert [f.path for f in bound_query.fields] == ["fa", "fd", "fn"]

    def test_calculated_fields(self, bound_query):
        assert bound_query.calculated_fields == {"fn"}

    def test_sort_fields(self, bound_query):
        assert [(f.path, f.direction, f.priority) for f in bound_query.sort_fields] == [
            ("fd", DSC, 0),
            ("fa", ASC, 1),
        ]

    def test_filters(self, bound_query):
        assert bound_query.filters == [
            BoundFilter([], "bob", None, "equals", "fred", StringFieldType)
        ]

    def test_bad_field(self, orm_models):
        query = Query("app.model", [QueryField("yata")], [])
        bound_query = BoundQuery(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_bad_fk(self, orm_models):
        query = Query("app.model", [QueryField("yata__yata")], [])
        bound_query = BoundQuery(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_bad_fk_field(self, orm_models):
        query = Query("app.model", [QueryField("tom__yata")], [])
        bound_query = BoundQuery(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_bad_fk_field_aggregate(self, orm_models):
        query = Query("app.model", [QueryField("tom__jones__yata")], [])
        bound_query = BoundQuery(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_bad_long_fk(self, orm_models):
        query = Query("app.model", [QueryField("yata__yata__yata")], [])
        bound_query = BoundQuery(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_aggregate(self, orm_models):
        query = Query("app.model", [QueryField("tom__jones__count")], [])
        bound_query = BoundQuery(query, orm_models)
        assert [f.path for f in bound_query.fields] == ["tom__jones__count"]

    def test_bad_filter(self, orm_models):
        query = Query("app.model", [], [QueryFilter("yata", "equals", "fred")])
        bound_query = BoundQuery(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_bad_filter_value(self, orm_models):
        query = Query(
            "app.model",
            [],
            [QueryFilter("num", "equals", "fred"), QueryFilter("num", "equals", 1)],
        )
        bound_query = BoundQuery(query, orm_models)
        assert [f.value for f in bound_query.filters] == ["fred", 1]
        assert [f.value for f in bound_query.valid_filters] == [1]


class TestBoundField:
    def test_path_properties(self, fake_orm_field):
        bf = BoundField(["bob", "fred"], "joe", "max", None, None, fake_orm_field)
        assert bf.model_path == "bob__fred"
        assert bf.field_path == "bob__fred__joe"
        assert bf.path == "bob__fred__joe__max"

        bf = BoundField([], "joe", "max", None, None, fake_orm_field)
        assert bf.model_path == ""
        assert bf.field_path == "joe"
        assert bf.path == "joe__max"

        bf = BoundField(["bob", "fred"], "joe", None, None, None, fake_orm_field)
        assert bf.model_path == "bob__fred"
        assert bf.field_path == "bob__fred__joe"
        assert bf.path == "bob__fred__joe"


class TestBoundFilter:
    def test_path_properties(self):
        bf = BoundFilter(["bob", "fred"], "joe", "max", "gt", 5, StringFieldType)
        assert bf.model_path == "bob__fred"
        assert bf.field_path == "bob__fred__joe"
        assert bf.path == "bob__fred__joe__max"

        bf = BoundFilter([], "joe", "max", "gt", 5, StringFieldType)
        assert bf.model_path == ""
        assert bf.field_path == "joe"
        assert bf.path == "joe__max"

        bf = BoundFilter(["bob", "fred"], "joe", None, "gt", 5, StringFieldType)
        assert bf.model_path == "bob__fred"
        assert bf.field_path == "bob__fred__joe"
        assert bf.path == "bob__fred__joe"


class TestFieldType:
    def test_repr(self):
        assert repr(StringFieldType) == f"StringFieldType"


class TestStringFieldType:
    def test_validate(self):
        assert BoundFilter(
            [], "bob", None, "contains", "hello", StringFieldType
        ).is_valid
        assert not BoundFilter(
            [], "bob", None, "pontains", "hello", StringFieldType
        ).is_valid

    def test_default_lookup(self):
        assert StringFieldType.default_lookup == "equals"

    def test_format(self):
        assert StringFieldType.format("bob") == "bob"


class TestNumberFieldType:
    def test_validate(self):
        assert BoundFilter([], "bob", None, "gt", "6.1", NumberFieldType).is_valid
        assert not BoundFilter(
            [], "bob", None, "pontains", "6.1", NumberFieldType
        ).is_valid
        assert not BoundFilter([], "bob", None, "gt", "hello", NumberFieldType).is_valid
        assert BoundFilter([], "bob", None, "is_null", "True", NumberFieldType).is_valid
        assert not BoundFilter(
            [], "bob", None, "is_null", "hello", NumberFieldType
        ).is_valid

    def test_default_lookup(self):
        assert NumberFieldType.default_lookup == "equals"

    def test_format(self):
        assert NumberFieldType.format(6) == 6


class TestTimeFieldType:
    def test_validate(self):
        assert BoundFilter(
            [], "bob", None, "gt", "2018-03-20T22:31:23", TimeFieldType
        ).is_valid
        assert not BoundFilter([], "bob", None, "gt", "hello", TimeFieldType).is_valid
        assert not BoundFilter(
            [], "bob", None, "pontains", "2018-03-20T22:31:23", TimeFieldType
        ).is_valid
        assert BoundFilter([], "bob", None, "is_null", "True", TimeFieldType).is_valid
        assert not BoundFilter(
            [], "bob", None, "is_null", "hello", TimeFieldType
        ).is_valid

    def test_default_lookup(self):
        assert TimeFieldType.default_lookup == "equals"

    def test_format(self):
        assert (
            TimeFieldType.format(timezone.make_aware(datetime(2020, 5, 19, 8, 42, 16)))
            == "2020-05-19 08:42:16"
        )


class TestBooleanFieldType:
    def test_validate(self):
        assert BoundFilter([], "bob", None, "equals", "True", BooleanFieldType).is_valid
        assert BoundFilter(
            [], "bob", None, "equals", "False", BooleanFieldType
        ).is_valid
        assert not BoundFilter(
            [], "bob", None, "equals", "hello", BooleanFieldType
        ).is_valid
        assert not BoundFilter(
            [], "bob", None, "pontains", "True", BooleanFieldType
        ).is_valid

    def test_default_lookup(self):
        assert BooleanFieldType.default_lookup == "equals"
