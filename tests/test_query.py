import re
from datetime import date, datetime, timedelta
from uuid import UUID

import pytest
import time_machine
from django.utils import timezone

from data_browser import orm_fields
from data_browser.orm_admin import OrmModel, get_fields_for_type
from data_browser.query import BoundQuery, Query, QueryField, QueryFilter
from data_browser.types import (
    ASC,
    DSC,
    BooleanType,
    DateTimeType,
    DateType,
    DurationType,
    HTMLType,
    IsNullType,
    NumberArrayType,
    NumberChoiceArrayType,
    NumberChoiceType,
    NumberType,
    RegexType,
    StringArrayType,
    StringChoiceArrayType,
    StringChoiceType,
    StringType,
    UnknownType,
    UUIDType,
)


@pytest.fixture
def query():
    return Query(
        "app.model",
        [
            QueryField("fa", False, ASC, 1),
            QueryField("fd", False, DSC, 0),
            QueryField("fn"),
        ],
        [QueryFilter("bob", "equals", "fred")],
    )


@pytest.fixture
def orm_models():
    return {
        "string": OrmModel(get_fields_for_type(StringType)),
        "number": OrmModel(get_fields_for_type(NumberType)),
        "app.model": OrmModel(
            fields={
                "fa": orm_fields.OrmConcreteField(
                    model_name="app.model",
                    name="fa",
                    pretty_name="fa",
                    type_=StringType,
                    rel_name=StringType.name,
                    choices=None,
                ),
                "fd": orm_fields.OrmConcreteField(
                    model_name="app.model",
                    name="fd",
                    pretty_name="fd",
                    type_=StringType,
                    rel_name=StringType.name,
                    choices=None,
                ),
                "fn": orm_fields.OrmCalculatedField(
                    model_name="app.model", name="fn", pretty_name="fn", func=None
                ),
                "bob": orm_fields.OrmConcreteField(
                    model_name="app.model",
                    name="bob",
                    pretty_name="bob",
                    type_=StringType,
                    rel_name=StringType.name,
                    choices=None,
                ),
                "num": orm_fields.OrmConcreteField(
                    model_name="app.model",
                    name="num",
                    pretty_name="num",
                    type_=NumberType,
                    rel_name=NumberType.name,
                    choices=None,
                ),
                "tom": orm_fields.OrmFkField(
                    model_name="app.model",
                    name="tom",
                    pretty_name="tom",
                    rel_name="app.Tom",
                    to_many=False,
                ),
            },
            admin=True,
        ),
        "app.Tom": OrmModel(
            fields={
                "jones": orm_fields.OrmConcreteField(
                    model_name="app.Tom",
                    name="jones",
                    pretty_name="jones",
                    type_=StringType,
                    rel_name=StringType.name,
                    choices=None,
                ),
                "michael": orm_fields.OrmFkField(
                    model_name="app.Tom",
                    name="michael",
                    pretty_name="michael",
                    rel_name="app.Michael",
                    to_many=False,
                ),
            },
            admin=True,
        ),
        "app.Michael": OrmModel(
            fields={
                "bolton": orm_fields.OrmConcreteField(
                    model_name="app.Michael",
                    name="bolton",
                    pretty_name="bolton",
                    type_=StringType,
                    rel_name=StringType.name,
                    choices=None,
                )
            },
            admin=True,
        ),
    }


@pytest.fixture
def bound_query(query, orm_models):
    return BoundQuery.bind(query, orm_models)


class ParseHelpers:
    choices = ()

    def check_parse(self, value, expected, error_re):
        res, err = self.type_.parse(value, self.choices)
        if expected is None:
            assert res is None
            assert re.fullmatch(error_re, err)
        else:
            assert err is None
            assert res == expected

    def check_parse_lookup(self, lookup, value, expected, error_re):
        res, err = self.type_.parse_lookup(lookup, value, self.choices)
        if expected is None:
            assert res is None
            assert re.fullmatch(error_re, err)
        else:
            assert err is None
            assert res == expected

    def check_format(self, value, expected):
        assert self.type_.get_formatter(self.choices)(value) == expected


class TestQuery:
    def test_from_request(self, query):
        q = Query.from_request("app.model", "fa+1,fd-0,fn", [("bob__equals", "fred")])
        assert q == query

    def test_from_request_duplicate_field(self, query):
        q = Query.from_request(
            "app.model", "fa+1,fd-0,fn,&fa-2", [("bob__equals", "fred")]
        )
        assert q == query

    def test_from_request_with_limit(self, query):
        q = Query.from_request(
            "app.model", "fa+1,fd-0,fn", [("limit", "123"), ("bob__equals", "fred")]
        )
        assert q.arguments["limit"] == 123

    def test_from_request_with_bad_limit(self, query):
        q = Query.from_request(
            "app.model", "fa+1,fd-0,fn", [("limit", "bob"), ("bob__equals", "fred")]
        )
        assert q.arguments["limit"] == 1000

    def test_from_request_with_low_limit(self, query):
        q = Query.from_request(
            "app.model", "fa+1,fd-0,fn", [("limit", "0"), ("bob__equals", "fred")]
        )
        assert q.arguments["limit"] == 1

    def test_from_request_with_related_filter(self):
        q = Query.from_request("app.model", "", [("bob__jones__equals", "fred")])
        assert q == Query(
            "app.model", [], [QueryFilter("bob__jones", "equals", "fred")]
        )

    def test_from_request_with_missing(self):
        q = Query.from_request("app.model", ",,", [])
        assert q == Query("app.model", [], [])

    def test_from_request_filter_no_value(self):
        q = Query.from_request("app.model", "", [("joe__equals", "")])
        assert q == Query("app.model", [], [QueryFilter("joe", "equals", "")])

    def test_from_request_filter_no_lookup(self):
        q = Query.from_request("app.model", "", [("joe", "tom")])
        assert q == Query("app.model", [], [], {"joe": "tom"})

    def test_from_request_filter_bad_lookup(self):
        q = Query.from_request("app.model", "", [("joe__blah", "123")])
        assert q == Query("app.model", [], [QueryFilter("joe", "blah", "123")])

    def test_from_request_filter_no_name(self):
        q = Query.from_request("app.model", "", [("", "123")])
        assert q == Query("app.model", [], [], {"": "123"})

    def test_from_request_field_no_name(self):
        q = Query.from_request("app.model", "+2", [])
        assert q == Query("app.model", [QueryField("", False, ASC, 2)], [])

    def test_from_request_field_no_priority(self):
        q = Query.from_request("app.model", "fn+", [])
        assert q == Query("app.model", [QueryField("fn")], [])

    def test_from_request_field_bad_priority(self):
        q = Query.from_request("app.model", "fn+x", [])
        assert q == Query("app.model", [QueryField("fn")], [])

    def test_from_request_field_pivoted(self):
        q = Query.from_request("app.model", "&fn", [])
        assert q == Query("app.model", [QueryField("fn", True)], [])

    def test_url(self, query):
        query.arguments = {"limit": "123"}
        assert (
            query.get_url("html")
            == "/query/app.model/fa+1,fd-0,fn.html?bob__equals=fred&limit=123"
        )
        assert (
            query.get_full_url("html")
            == "/data_browser/query/app.model/fa+1,fd-0,fn.html?bob__equals=fred&limit=123"
        )

    def test_url_no_filters(self, query):
        query.filters = []
        assert query.get_url("html") == "/query/app.model/fa+1,fd-0,fn.html?limit=1000"
        assert (
            query.get_full_url("html")
            == "/data_browser/query/app.model/fa+1,fd-0,fn.html?limit=1000"
        )


class TestBoundQuery:
    def test_fields(self, bound_query):
        assert [f.path for f in bound_query.fields] == [["fa"], ["fd"], ["fn"]]

    def test_sort_fields(self, bound_query):
        assert [(f.path, f.direction, f.priority) for f in bound_query.sort_fields] == [
            (["fd"], DSC, 0),
            (["fa"], ASC, 1),
        ]

    def test_bad_field(self, orm_models):
        query = Query("app.model", [QueryField("yata")], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_bad_field_lookup(self, orm_models):
        query = Query("app.model", [QueryField("fa__count__bob")], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_bad_fk(self, orm_models):
        query = Query("app.model", [QueryField("yata__yata")], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_bad_fk_field(self, orm_models):
        query = Query("app.model", [QueryField("tom__yata")], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_bad_fk_field_aggregate(self, orm_models):
        query = Query("app.model", [QueryField("tom__jones__yata")], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_bad_long_fk(self, orm_models):
        query = Query("app.model", [QueryField("yata__yata__yata")], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_aggregate(self, orm_models):
        query = Query("app.model", [QueryField("tom__jones__count")], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.fields] == [["tom", "jones", "count"]]

    def test_piovt_aggregate(self, orm_models):
        query = Query("app.model", [QueryField("tom__jones__count", pivoted=True)], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.pivoted for f in bound_query.fields] == [False]

    def test_piovt(self, orm_models):
        query = Query("app.model", [QueryField("tom__jones", pivoted=True)], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.pivoted for f in bound_query.fields] == [True]

    def test_bad_filter(self, orm_models):
        query = Query("app.model", [], [QueryFilter("yata", "equals", "fred")])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.filters] == [["yata"]]

    def test_bad_filter_value(self, orm_models):
        query = Query(
            "app.model",
            [],
            [QueryFilter("num", "equals", "fred"), QueryFilter("num", "equals", 1)],
        )
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.value for f in bound_query.filters] == ["fred", 1]
        assert [f.value for f in bound_query.valid_filters] == [1]

    def test_fk(self, orm_models):
        query = Query("app.model", [QueryField("tom")], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_filter_calculated_field(self, orm_models):
        query = Query("app.model", [], [QueryFilter("fn", "equals", "fred")])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.filters] == [["fn"]]


class TestType:
    def test_repr(self):
        assert repr(StringType) == "StringType"


class TestRegexType(ParseHelpers):
    type_ = RegexType

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "value,expected,err", [(".*", ".*", None), ("\\", None, "Invalid regex")]
    )
    def test_parse(self, value, expected, err):
        self.check_parse(value, expected, err)


class TestStringType(ParseHelpers):
    type_ = StringType

    def test_default_lookup(self):
        assert StringType.default_lookup == "equals"

    @pytest.mark.parametrize("value,expected", [("bob", "bob"), (None, None)])
    def test_format(self, value, expected):
        self.check_format(value, expected)


class TestNumberType(ParseHelpers):
    type_ = NumberType

    @pytest.mark.parametrize(
        "value,expected,err",
        [
            ("6.1", 6.1, None),
            ("hello", None, "Could not convert string to float: 'hello'"),
        ],
    )
    def test_parse(self, value, expected, err):
        self.check_parse(value, expected, err)

    def test_default_lookup(self):
        assert self.type_.default_lookup == "equals"

    @pytest.mark.parametrize("value,expected", [(6, 6), (None, None)])
    def test_format(self, value, expected):
        self.check_format(value, expected)


def dt(Y, M, D, h=0, m=0, s=0):
    return datetime(Y, M, D, h, m, s, tzinfo=timezone.utc)


class TestDateTimeType(ParseHelpers):
    type_ = DateTimeType

    @time_machine.travel("2020-12-13 09:42:53", tick=False)
    @pytest.mark.parametrize(
        "value,expected,err",
        [
            ("2018-03-20T22:31:23", dt(2018, 3, 20, 22, 31, 23), None),
            ("2018-3-2T22:31:23", dt(2018, 3, 2, 22, 31, 23), None),
            ("hello", None, "Unrecognized clause 'hello'"),
            ("now", dt(2020, 12, 13, 9, 42, 53), None),
            # dateutil.parser
            ("11-11-2018", dt(2018, 11, 11), None),
            ("11-22-2018", dt(2018, 11, 22), None),
            ("21-12-2018", dt(2018, 12, 21), None),
            ("11-12-2018", None, "Ambiguous value"),
            ("21-22-2018", None, "Unrecognized clause '21-22-2018'"),
            ("2018-11-11", dt(2018, 11, 11), None),
            ("2018-11-22", dt(2018, 11, 22), None),
            ("2018-21-12", None, "Month must be in 1..12: 2018-21-12"),
            ("2018-11-12", dt(2018, 11, 12), None),
            ("2018-21-22", None, "Month must be in 1..12: 2018-21-22"),
            ("2018-3-2", dt(2018, 3, 2), None),
            ("20181111", dt(2018, 11, 11), None),
            ("20181122", dt(2018, 11, 22), None),
            ("20182112", None, "Month must be in 1..12: 20182112"),
            ("20181112", dt(2018, 11, 12), None),
            ("20182122", None, "Month must be in 1..12: 20182122"),
            ("181111", None, "Ambiguous value"),
            ("181122", None, "Ambiguous value"),
            ("182112", None, "Unrecognized clause '182112'"),
            ("181112", None, "Ambiguous value"),
            ("182122", None, "Unrecognized clause '182122'"),
            ("111118", None, "Ambiguous value"),
            ("112218", dt(2018, 11, 22), None),
            ("211218", None, "Ambiguous value"),
            ("111218", None, "Ambiguous value"),
            ("212218", None, "Unrecognized clause '212218'"),
            # dateutil.relativedelta
            ("hour+1", dt(2020, 12, 13, 10, 42, 53), None),
            ("hour-1", dt(2020, 12, 13, 8, 42, 53), None),
            ("hour=1", dt(2020, 12, 13, 1, 42, 53), None),
            ("hour 1", None, "Unrecognized clause 'hour'"),
            ("hour+0", dt(2020, 12, 13, 9, 42, 53), None),
            ("hour=0", dt(2020, 12, 13, 0, 42, 53), None),
            ("month+1", dt(2021, 1, 13, 9, 42, 53), None),
            ("month-1", dt(2020, 11, 13, 9, 42, 53), None),
            ("month=1", dt(2020, 1, 13, 9, 42, 53), None),
            ("month 1", None, "Unrecognized clause 'month'"),
            ("month+0", dt(2020, 12, 13, 9, 42, 53), None),
            ("month=0", None, "Can't set 'month' to '0'"),
            ("thurs+1", dt(2020, 12, 17, 9, 42, 53), None),
            ("thurs-1", dt(2020, 12, 10, 9, 42, 53), None),
            ("thurs=1", None, "'=' not supported for 'thurs'"),
            ("thurs 1", None, "Unrecognized clause 'thurs'"),
            ("thurs+0", None, "Can't add '0' 'thurs's"),
            ("thurs=0", None, "'=' not supported for 'thurs'"),
            ("month+1 month=1", dt(2021, 1, 13, 9, 42, 53), None),
            ("month=1 month+1", dt(2020, 2, 13, 9, 42, 53), None),
            ("bobit+1", None, "Unrecognized field 'bobit'"),
            ("week=1", None, "'=' not supported for 'week'"),
        ],
    )
    def test_parse(self, value, expected, err):
        self.check_parse(value, expected, err)

    def test_default_lookup(self):
        assert DateTimeType.default_lookup == "equals"

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "value,expected",
        [
            (
                datetime(2020, 5, 19, 8, 42, 16, tzinfo=timezone.utc),
                "2020-05-19 08:42:16",
            ),
            (None, None),
        ],
    )
    def test_aware_format(self, value, expected, settings):
        settings.USE_TZ = True
        self.check_format(value, expected)

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "value,expected",
        [(datetime(2020, 5, 19, 8, 42, 16), "2020-05-19 08:42:16"), (None, None)],
    )
    def test_naive_format(self, value, expected, settings):
        settings.USE_TZ = False
        self.check_format(value, expected)


class TestDurationType(ParseHelpers):
    type_ = DurationType

    @pytest.mark.parametrize(
        "value,expected,err",
        [
            ("5 days", timedelta(days=5), None),
            ("5 5:5", timedelta(days=5, hours=5, minutes=5), None),
            ("5 dayss", None, "Duration value should be 'DD HH:MM:SS'"),
        ],
    )
    def test_parse(self, value, expected, err):
        self.check_parse(value, expected, err)

    def test_default_lookup(self):
        assert self.type_.default_lookup == "equals"

    @pytest.mark.parametrize(
        "value,expected",
        [
            (timedelta(days=5, minutes=6), "5 days, 0:06:00"),
            (timedelta(minutes=6), "0:06:00"),
            (None, None),
        ],
    )
    def test_format(self, value, expected):
        self.check_format(value, expected)


class TestDateType(ParseHelpers):
    type_ = DateType

    @time_machine.travel("2020-12-13 09:42:53", tick=False)
    @pytest.mark.parametrize(
        "value,expected,err",
        [
            ("2018-03-20T22:31:23", dt(2018, 3, 20).date(), None),
            ("hello", None, "Unrecognized clause 'hello'"),
            ("today", dt(2020, 12, 13).date(), None),
            ("11-22-2018", dt(2018, 11, 22).date(), None),
            ("21-12-2018", dt(2018, 12, 21).date(), None),
            ("11-12-2018", None, "Ambiguous value"),
            ("21-22-2018", None, "Unrecognized clause '21-22-2018'"),
            ("days+1", dt(2020, 12, 14).date(), None),
        ],
    )
    def test_parse(self, value, expected, err):
        self.check_parse(value, expected, err)

    def test_default_lookup(self):
        assert self.type_.default_lookup == "equals"

    @pytest.mark.parametrize(
        "value,expected", [(date(2020, 5, 19), "2020-05-19"), (None, None)]
    )
    def test_format(self, value, expected):
        self.check_format(value, expected)


class TestBooleanType(ParseHelpers):
    type_ = BooleanType

    @pytest.mark.parametrize(
        "value,expected,err",
        [
            ("True", True, None),
            ("False", False, None),
            ("hello", None, "Expected 'true' or 'false'"),
        ],
    )
    def test_parse(self, value, expected, err):
        self.check_parse(value, expected, err)

    @pytest.mark.parametrize("value,expected", [(None, None)])
    def test_format(self, value, expected):
        self.check_format(value, expected)

    def test_default_lookup(self):
        assert self.type_.default_lookup == "equals"


class TestStringChoiceType(ParseHelpers):
    type_ = StringChoiceType
    choices = [("a", "A"), ("b", "B"), ("c", "C")]

    @pytest.mark.parametrize("value,expected", [("b", "B"), (None, None)])
    def test_format(self, value, expected):
        self.check_format(value, expected)

    def test_bad_value(self):
        assert self.type_.get_formatter(self.choices)("x") == "x"

    @pytest.mark.parametrize(
        "value,expected,err", [("B", "b", None), ("X", None, "Unknown choice 'X'")]
    )
    def test_parse(self, value, expected, err):
        self.check_parse(value, expected, err)


class TestNumberChoiceType(ParseHelpers):
    type_ = NumberChoiceType
    choices = [(1, "A"), (2, "B"), (3, "C")]

    @pytest.mark.parametrize("value,expected", [(2, "B"), (None, None)])
    def test_format(self, value, expected):
        self.check_format(value, expected)

    def test_bad_value(self):
        assert self.type_.get_formatter(self.choices)(6) == 6

    @pytest.mark.parametrize(
        "value,expected,err", [("B", 2, None), ("X", None, "Unknown choice 'X'")]
    )
    def test_parse(self, value, expected, err):
        self.check_parse(value, expected, err)


class TestHTMLType(ParseHelpers):
    type_ = HTMLType

    @pytest.mark.parametrize("value,expected", [(None, None)])
    def test_format(self, value, expected):
        self.check_format(value, expected)


class TestIsNullType(ParseHelpers):
    type_ = IsNullType

    @pytest.mark.parametrize(
        "value,expected", [(True, "IsNull"), (False, "NotNull"), (None, "IsNull")]
    )
    def test_format(self, value, expected):
        self.check_format(value, expected)

    @pytest.mark.parametrize(
        "value,expected,err", [("IsNull", True, None), ("NotNull", False, None)]
    )
    def test_parse(self, value, expected, err):
        self.check_parse(value, expected, err)


class TestUUIDType(ParseHelpers):
    type_ = UUIDType
    s = "210081a4-7315-4173-aa73-4bab47b2f9a5"
    u = UUID(s)

    @pytest.mark.parametrize("value,expected", [(u, s), (None, None)])
    def test_format(self, value, expected):
        self.check_format(value, expected)

    @pytest.mark.parametrize(
        "value,expected,err",
        [
            (s, u, None),
            (s.replace("-", ""), u, None),
            (s[1:], None, "Badly formed hexadecimal UUID string"),
        ],
    )
    def test_parse(self, value, expected, err):
        self.check_parse(value, expected, err)


class TestUnknownType(ParseHelpers):
    type_ = UnknownType

    @pytest.mark.parametrize("value,expected", [(None, None)])
    def test_format(self, value, expected):
        self.check_format(value, expected)


class TestStringArrayType(ParseHelpers):
    type_ = StringArrayType

    @pytest.mark.parametrize(
        "value,expected,err",
        [('["bob"]', ["bob"], None), ('"bob"', None, "Expected a list")],
    )
    def test_parse(self, value, expected, err):
        self.check_parse(value, expected, err)


class TestStringChoiceArrayType(ParseHelpers):
    type_ = StringChoiceArrayType
    choices = [("fred", "bob")]

    @pytest.mark.parametrize(
        "value,expected,err",
        [('["bob"]', ["fred"], None), ('"bob"', None, "Expected a list")],
    )
    def test_parse(self, value, expected, err):
        self.check_parse(value, expected, err)

    @pytest.mark.parametrize(
        "lookup,value,expected,err",
        [("contains", "bob", "fred", None), ("length", "1", 1, None)],
    )
    def test_parse_lookup(self, lookup, value, expected, err):
        self.check_parse_lookup(lookup, value, expected, err)


class TestNumberArrayType(ParseHelpers):
    type_ = NumberArrayType

    @pytest.mark.parametrize(
        "value,expected,err", [("[123]", [123], None), ("123", None, "Expected a list")]
    )
    def test_parse(self, value, expected, err):
        self.check_parse(value, expected, err)


class TestNumberChoiceArrayType(ParseHelpers):
    type_ = NumberChoiceArrayType
    choices = [(123, "bob")]

    @pytest.mark.parametrize(
        "value,expected,err",
        [('["bob"]', [123], None), ('"bob"', None, "Expected a list")],
    )
    def test_parse(self, value, expected, err):
        self.check_parse(value, expected, err)

    @pytest.mark.parametrize(
        "lookup,value,expected,err",
        [("contains", "bob", 123, None), ("length", "1", 1, None)],
    )
    def test_parse_lookup(self, lookup, value, expected, err):
        self.check_parse_lookup(lookup, value, expected, err)
