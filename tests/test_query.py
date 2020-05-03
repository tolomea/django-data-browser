import pytest
from data_browser import orm
from data_browser.query import (
    ASC,
    DSC,
    BooleanFieldType,
    BoundFilter,
    BoundQuery,
    NumberFieldType,
    Query,
    QueryField,
    QueryFilter,
    StringFieldType,
    TimeFieldType,
)


@pytest.fixture
def query():
    return Query(
        "app.model",
        [QueryField("fa", ASC, 1), QueryField("fd", DSC, 0), QueryField("fn")],
        [QueryFilter("bob", "equals", "fred")],
    )


@pytest.fixture
def bound_query(query):
    orm_models = {
        "app.model": orm.OrmModel(
            fields={
                "fa": orm.OrmField(type_=StringFieldType, concrete=True),
                "fd": orm.OrmField(type_=StringFieldType, concrete=True),
                "fn": orm.OrmField(type_=StringFieldType, concrete=False),
                "bob": orm.OrmField(type_=StringFieldType, concrete=True),
            },
            fks={"tom": "app.Tom"},
        ),
        "app.Tom": orm.OrmModel(
            fields={"jones": orm.OrmField(type_=StringFieldType, concrete=True)},
            fks={"michael": "app.Michael"},
        ),
        "app.Michael": orm.OrmModel(
            fields={"bolton": orm.OrmField(type_=StringFieldType, concrete=True)},
            fks={},
        ),
    }
    return BoundQuery(query, orm_models)


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
            BoundFilter("bob", "equals", "fred", StringFieldType)
        ]


class TestFieldType:
    def test_repr(self):
        assert repr(StringFieldType) == f"StringFieldType"


class TestStringFieldType:
    def test_validate(self):
        assert BoundFilter("bob", "contains", "hello", StringFieldType).is_valid
        assert not BoundFilter("bob", "pontains", "hello", StringFieldType).is_valid

    def test_default_lookup(self):
        assert StringFieldType.default_lookup == "equals"


class TestNumberFieldType:
    def test_validate(self):
        assert BoundFilter("bob", "gt", "6.1", NumberFieldType).is_valid
        assert not BoundFilter("bob", "pontains", "6.1", NumberFieldType).is_valid
        assert not BoundFilter("bob", "gt", "hello", NumberFieldType).is_valid
        assert BoundFilter("bob", "is_null", "True", NumberFieldType).is_valid
        assert not BoundFilter("bob", "is_null", "hello", NumberFieldType).is_valid

    def test_default_lookup(self):
        assert NumberFieldType.default_lookup == "equals"


class TestTimeFieldType:
    def test_validate(self):
        assert BoundFilter("bob", "gt", "2018-03-20T22:31:23", TimeFieldType).is_valid
        assert not BoundFilter("bob", "gt", "hello", TimeFieldType).is_valid
        assert not BoundFilter(
            "bob", "pontains", "2018-03-20T22:31:23", TimeFieldType
        ).is_valid
        assert BoundFilter("bob", "is_null", "True", TimeFieldType).is_valid
        assert not BoundFilter("bob", "is_null", "hello", TimeFieldType).is_valid

    def test_default_lookup(self):
        assert TimeFieldType.default_lookup == "equals"


class TestBooleanFieldType:
    def test_validate(self):
        assert BoundFilter("bob", "equals", "True", BooleanFieldType).is_valid
        assert not BoundFilter("bob", "equals", "hello", BooleanFieldType).is_valid
        assert not BoundFilter("bob", "pontains", "True", BooleanFieldType).is_valid

    def test_default_lookup(self):
        assert BooleanFieldType.default_lookup == "equals"
