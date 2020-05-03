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
    StringFieldType,
    TimeFieldType,
)


@pytest.fixture
def query():
    return Query(
        "app.model", {"fa": ASC, "fd": DSC, "fn": None}, [("bob", "equals", "fred")]
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


@pytest.fixture
def filter(query):
    return BoundFilter("bob", 0, StringFieldType, "equals", "fred")


class TestQuery:
    def test_from_request(self, query):
        q = Query.from_request("app.model", "+fa,-fd,fn", {"bob__equals": ["fred"]})
        assert q == query

    def test_from_request_with_related_filter(self):
        q = Query.from_request(
            "app.model", "+fa,-fd,fn", {"bob__jones__equals": ["fred"]}
        )
        assert q == Query(
            "app.model",
            {"fa": ASC, "fd": DSC, "fn": None},
            [("bob__jones", "equals", "fred")],
        )

    def test_url(self, query):
        assert (
            query.get_url("html")
            == "/data_browser/query/app.model/+fa,-fd,fn.html?bob__equals=fred"
        )

    def test_url_no_filters(self, query):
        query.filters = []
        assert query.get_url("html") == "/data_browser/query/app.model/+fa,-fd,fn.html?"


class TestBoundQuery:
    def test_fields(self, bound_query):
        assert [f.path for f in bound_query.fields] == ["fa", "fd", "fn"]

    def test_calculated_fields(self, bound_query):
        assert bound_query.calculated_fields == {"fn"}

    def test_sort_fields(self, bound_query):
        assert [(f.path, f.direction) for f in bound_query.sort_fields] == [
            ("fa", ASC),
            ("fd", DSC),
        ]

    def test_filters(self, bound_query, filter):
        assert list(bound_query.filters) == [filter]


class TestFieldType:
    def test_repr(self):
        assert repr(StringFieldType) == f"StringFieldType"


class TestStringFieldType:
    def test_validate(self):
        assert BoundFilter("bob", 0, StringFieldType, "contains", "hello").is_valid
        assert not BoundFilter("bob", 0, StringFieldType, "pontains", "hello").is_valid

    def test_default_lookup(self):
        assert StringFieldType.default_lookup == "equals"


class TestNumberFieldType:
    def test_validate(self):
        assert BoundFilter("bob", 0, NumberFieldType, "gt", "6.1").is_valid
        assert not BoundFilter("bob", 0, NumberFieldType, "pontains", "6.1").is_valid
        assert not BoundFilter("bob", 0, NumberFieldType, "gt", "hello").is_valid
        assert BoundFilter("bob", 0, NumberFieldType, "is_null", "True").is_valid
        assert not BoundFilter("bob", 0, NumberFieldType, "is_null", "hello").is_valid

    def test_default_lookup(self):
        assert NumberFieldType.default_lookup == "equals"


class TestTimeFieldType:
    def test_validate(self):
        assert BoundFilter(
            "bob", 0, TimeFieldType, "gt", "2018-03-20T22:31:23"
        ).is_valid
        assert not BoundFilter("bob", 0, TimeFieldType, "gt", "hello").is_valid
        assert not BoundFilter(
            "bob", 0, TimeFieldType, "pontains", "2018-03-20T22:31:23"
        ).is_valid
        assert BoundFilter("bob", 0, TimeFieldType, "is_null", "True").is_valid
        assert not BoundFilter("bob", 0, TimeFieldType, "is_null", "hello").is_valid

    def test_default_lookup(self):
        assert TimeFieldType.default_lookup == "equals"


class TestBooleanFieldType:
    def test_validate(self):
        assert BoundFilter("bob", 0, BooleanFieldType, "equals", "True").is_valid
        assert not BoundFilter("bob", 0, BooleanFieldType, "equals", "hello").is_valid
        assert not BoundFilter("bob", 0, BooleanFieldType, "pontains", "True").is_valid

    def test_default_lookup(self):
        assert BooleanFieldType.default_lookup == "equals"
