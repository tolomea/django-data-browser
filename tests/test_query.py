from datetime import date, datetime

import pytest
from data_browser import orm
from data_browser.query import (
    ASC,
    DSC,
    BooleanFieldType,
    BoundFilter,
    BoundQuery,
    DateFieldType,
    DateTimeFieldType,
    MonthFieldType,
    NumberFieldType,
    Query,
    QueryField,
    QueryFilter,
    StringFieldType,
    WeekDayFieldType,
)
from django.http import QueryDict
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
        "string": orm._get_fields_for_type(StringFieldType),
        "number": orm._get_fields_for_type(NumberFieldType),
        "app.model": orm.OrmModel(
            fields={
                "fa": orm.OrmConcreteField(
                    model_name="app.model",
                    name="fa",
                    pretty_name="fa",
                    type_=StringFieldType,
                ),
                "fd": orm.OrmConcreteField(
                    model_name="app.model",
                    name="fd",
                    pretty_name="fd",
                    type_=StringFieldType,
                ),
                "fn": orm.OrmCalculatedField(
                    model_name="app.model", name="fn", pretty_name="fn"
                ),
                "bob": orm.OrmConcreteField(
                    model_name="app.model",
                    name="bob",
                    pretty_name="bob",
                    type_=StringFieldType,
                ),
                "num": orm.OrmConcreteField(
                    model_name="app.model",
                    name="num",
                    pretty_name="num",
                    type_=NumberFieldType,
                ),
                "tom": orm.OrmFkField(
                    model_name="app.model",
                    name="tom",
                    pretty_name="tom",
                    rel_name="app.Tom",
                ),
            },
            admin=True,
        ),
        "app.Tom": orm.OrmModel(
            fields={
                "jones": orm.OrmConcreteField(
                    model_name="app.Tom",
                    name="jones",
                    pretty_name="jones",
                    type_=StringFieldType,
                ),
                "michael": orm.OrmFkField(
                    model_name="app.Tom",
                    name="michael",
                    pretty_name="michael",
                    rel_name="app.Michael",
                ),
            },
            admin=True,
        ),
        "app.Michael": orm.OrmModel(
            fields={
                "bolton": orm.OrmConcreteField(
                    model_name="app.Michael",
                    name="bolton",
                    pretty_name="bolton",
                    type_=StringFieldType,
                )
            },
            admin=True,
        ),
    }


@pytest.fixture
def bound_query(query, orm_models):
    return BoundQuery(query, orm_models)


class TestQuery:
    def test_from_request(self, query):
        q = Query.from_request(
            "app.model", "fa+1,fd-0,fn", QueryDict("bob__equals=fred")
        )
        assert q == query

    def test_from_request_with_related_filter(self):
        q = Query.from_request("app.model", "", QueryDict("bob__jones__equals=fred"))
        assert q == Query(
            "app.model", [], [QueryFilter("bob__jones", "equals", "fred")]
        )

    def test_from_request_with_missing(self):
        q = Query.from_request("app.model", ",,", QueryDict(""))
        assert q == Query("app.model", [], [])

    def test_from_request_filter_no_value(self):
        q = Query.from_request("app.model", "", QueryDict("joe__equals="))
        assert q == Query("app.model", [], [QueryFilter("joe", "equals", "")])

    def test_from_request_filter_no_lookup(self):
        q = Query.from_request("app.model", "", QueryDict("joe=tom"))
        assert q == Query("app.model", [], [])

    def test_from_request_filter_bad_lookup(self):
        q = Query.from_request("app.model", "", QueryDict("joe__blah=123"))
        assert q == Query("app.model", [], [QueryFilter("joe", "blah", "123")])

    def test_from_request_filter_no_name(self):
        q = Query.from_request("app.model", "", QueryDict("=123"))
        assert q == Query("app.model", [], [])

    def test_from_request_field_no_name(self):
        q = Query.from_request("app.model", "+2", QueryDict(""))
        assert q == Query("app.model", [QueryField("", ASC, 2)], [])

    def test_from_request_field_no_priority(self):
        q = Query.from_request("app.model", "fn+", QueryDict(""))
        assert q == Query("app.model", [QueryField("fn", None, None)], [])

    def test_from_request_field_bad_priority(self):
        q = Query.from_request("app.model", "fn+x", QueryDict(""))
        assert q == Query("app.model", [QueryField("fn", None, None)], [])

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
        assert [f.path for f in bound_query.fields] == [["fa"], ["fd"], ["fn"]]

    def test_sort_fields(self, bound_query):
        assert [(f.path, f.direction, f.priority) for f in bound_query.sort_fields] == [
            (["fd"], DSC, 0),
            (["fa"], ASC, 1),
        ]

    def test_filters(self, bound_query, orm_models):
        orm_field = orm_models["app.model"].fields["bob"]
        assert bound_query.filters == [
            BoundFilter(
                orm.OrmBoundField(orm_field, orm_field, [], ["bob"]), "equals", "fred"
            )
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
        assert [f.path for f in bound_query.fields] == [["tom", "jones", "count"]]

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

    def test_fk(self, orm_models):
        query = Query("app.model", [QueryField("tom")], [])
        bound_query = BoundQuery(query, orm_models)
        assert [f.path for f in bound_query.fields] == []


class TestFieldType:
    def test_repr(self):
        assert repr(StringFieldType) == f"StringFieldType"


class TestStringFieldType:
    def test_validate(self):
        orm_field = orm.OrmConcreteField("", "bob", "bob", StringFieldType)
        orm_bound_field = orm.OrmBoundField(orm_field, orm_field.type_, [], ["bob"])
        assert BoundFilter(orm_bound_field, "contains", "hello").is_valid
        assert not BoundFilter(orm_bound_field, "pontains", "hello").is_valid

    def test_default_lookup(self):
        assert StringFieldType.default_lookup == "equals"

    def test_format(self):
        assert StringFieldType.format("bob") == "bob"


class TestNumberFieldType:
    def test_validate(self):
        orm_field = orm.OrmConcreteField("", "bob", "bob", NumberFieldType)
        orm_bound_field = orm.OrmBoundField(orm_field, orm_field.type_, [], ["bob"])
        assert BoundFilter(orm_bound_field, "gt", "6.1").is_valid
        assert not BoundFilter(orm_bound_field, "pontains", "6.1").is_valid
        assert not BoundFilter(orm_bound_field, "gt", "hello").is_valid
        assert BoundFilter(orm_bound_field, "is_null", "True").is_valid
        assert not BoundFilter(orm_bound_field, "is_null", "hello").is_valid

    def test_default_lookup(self):
        assert NumberFieldType.default_lookup == "equals"

    def test_format(self):
        assert NumberFieldType.format(6) == 6


class TestDateTimeFieldType:
    def test_validate(self):
        orm_field = orm.OrmConcreteField("", "bob", "bob", DateTimeFieldType)
        orm_bound_field = orm.OrmBoundField(orm_field, orm_field.type_, [], ["bob"])
        assert BoundFilter(orm_bound_field, "gt", "2018-03-20T22:31:23").is_valid
        assert not BoundFilter(orm_bound_field, "gt", "hello").is_valid
        assert not BoundFilter(
            orm_bound_field, "pontains", "2018-03-20T22:31:23"
        ).is_valid
        assert BoundFilter(orm_bound_field, "is_null", "True").is_valid
        assert not BoundFilter(orm_bound_field, "is_null", "hello").is_valid
        assert BoundFilter(orm_bound_field, "gt", "now").is_valid

    def test_default_lookup(self):
        assert DateTimeFieldType.default_lookup == "equals"

    def test_format(self):
        assert (
            DateTimeFieldType.format(
                timezone.make_aware(datetime(2020, 5, 19, 8, 42, 16))
            )
            == "2020-05-19 08:42:16"
        )


class TestDateFieldType:
    def test_validate(self):
        orm_field = orm.OrmConcreteField("", "bob", "bob", DateFieldType)
        orm_bound_field = orm.OrmBoundField(orm_field, orm_field.type_, [], ["bob"])
        assert BoundFilter(orm_bound_field, "gt", "2018-03-20T22:31:23").is_valid
        assert not BoundFilter(orm_bound_field, "gt", "hello").is_valid
        assert not BoundFilter(
            orm_bound_field, "pontains", "2018-03-20T22:31:23"
        ).is_valid
        assert BoundFilter(orm_bound_field, "is_null", "True").is_valid
        assert not BoundFilter(orm_bound_field, "is_null", "hello").is_valid
        assert BoundFilter(orm_bound_field, "gt", "today").is_valid

    def test_default_lookup(self):
        assert DateFieldType.default_lookup == "equals"

    def test_format(self):
        assert DateFieldType.format(date(2020, 5, 19)) == "2020-05-19"


class TestWeekDayFieldType:
    def test_format(self):
        assert WeekDayFieldType.format(None) is None
        assert WeekDayFieldType.format(1) == "Sunday"
        assert WeekDayFieldType.format(7) == "Saturday"


class TestMonthFieldType:
    def test_format(self):
        assert MonthFieldType.format(None) is None
        assert MonthFieldType.format(1) == "January"
        assert MonthFieldType.format(12) == "December"


class TestBooleanFieldType:
    def test_validate(self):
        orm_field = orm.OrmConcreteField("", "bob", "bob", BooleanFieldType)
        orm_bound_field = orm.OrmBoundField(orm_field, orm_field.type_, [], ["bob"])
        assert BoundFilter(orm_bound_field, "equals", "True").is_valid
        assert BoundFilter(orm_bound_field, "equals", "False").is_valid
        assert not BoundFilter(orm_bound_field, "equals", "hello").is_valid
        assert not BoundFilter(orm_bound_field, "pontains", "True").is_valid

    def test_default_lookup(self):
        assert BooleanFieldType.default_lookup == "equals"
