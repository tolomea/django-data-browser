import pytest
from data_browser.query import (
    ASC,
    DSC,
    BooleanField,
    BoundQuery,
    CalculatedField,
    Filter,
    NumberField,
    Query,
    StringField,
    TimeField,
)


@pytest.fixture
def query():
    return Query(
        "app",
        "model",
        {"fa": ASC, "fd": DSC, "fn": None},
        "html",
        [("bob", "equals", "fred")],
    )


@pytest.fixture
def bound_query(query):
    all_model_fields = {
        "app.model": {
            "fields": {
                "fa": StringField,
                "fd": StringField,
                "fn": StringField,
                "bob": StringField,
            },
            "fks": {"tom": "app.Tom"},
        },
        "app.Tom": {
            "fields": {"jones": StringField},
            "fks": {"michael": "app.Michael"},
        },
        "app.Michael": {"fields": {"bolton": StringField}, "fks": {}},
    }
    return BoundQuery(query, "app.model", all_model_fields)


@pytest.fixture
def filter(query):
    return Filter("bob", 0, StringField, "equals", "fred")


class TestQuery:
    def test_from_request(self, query):
        q = Query.from_request(
            "app", "model", "+fa,-fd,fn", "html", {"bob__equals": ["fred"]}
        )
        assert q == query

    def test_from_request_with_related_filter(self):
        q = Query.from_request(
            "app", "model", "+fa,-fd,fn", "html", {"bob__jones__equals": ["fred"]}
        )
        assert q == Query(
            "app",
            "model",
            {"fa": ASC, "fd": DSC, "fn": None},
            "html",
            [("bob__jones", "equals", "fred")],
        )

    def test_url(self, query):
        assert (
            query.url
            == "/data_browser/query/app.model/+fa,-fd,fn.html?bob__equals=fred"
        )

    def test_url_no_filters(self, query):
        query.filters = []
        assert query.url == "/data_browser/query/app.model/+fa,-fd,fn.html?"


class TestBoundQuery:
    def test_fields(self, bound_query):
        assert list(bound_query.fields) == ["fa", "fd", "fn"]

    def test_calculated_fields(self, bound_query):
        assert list(bound_query.calculated_fields) == []
        bound_query.all_model_fields["app.model"]["fields"]["fa"] = CalculatedField
        assert list(bound_query.calculated_fields) == ["fa"]

    def test_sort_fields(self, bound_query):
        assert list(bound_query.sort_fields) == [
            ("fa", StringField, ASC),
            ("fd", StringField, DSC),
            ("fn", StringField, None),
        ]

    def test_filters(self, bound_query, filter):
        assert list(bound_query.filters) == [filter]


class TestField:
    def test_repr(self):
        assert repr(StringField) == f"StringField"


class TestStringField:
    def test_validate(self):
        assert Filter("bob", 0, StringField, "contains", "hello").is_valid
        assert not Filter("bob", 0, StringField, "pontains", "hello").is_valid

    def test_default_lookup(self):
        assert StringField.default_lookup == "equals"


class TestNumberField:
    def test_validate(self):
        assert Filter("bob", 0, NumberField, "gt", "6.1").is_valid
        assert not Filter("bob", 0, NumberField, "pontains", "6.1").is_valid
        assert not Filter("bob", 0, NumberField, "gt", "hello").is_valid
        assert Filter("bob", 0, NumberField, "is_null", "True").is_valid
        assert not Filter("bob", 0, NumberField, "is_null", "hello").is_valid

    def test_default_lookup(self):
        assert NumberField.default_lookup == "equals"


class TestTimeField:
    def test_validate(self):
        assert Filter("bob", 0, TimeField, "gt", "2018-03-20T22:31:23").is_valid
        assert not Filter("bob", 0, TimeField, "gt", "hello").is_valid
        assert not Filter(
            "bob", 0, TimeField, "pontains", "2018-03-20T22:31:23"
        ).is_valid
        assert Filter("bob", 0, TimeField, "is_null", "True").is_valid
        assert not Filter("bob", 0, TimeField, "is_null", "hello").is_valid

    def test_default_lookup(self):
        assert TimeField.default_lookup == "equals"


class TestBooleanField:
    def test_validate(self):
        assert Filter("bob", 0, BooleanField, "equals", "True").is_valid
        assert not Filter("bob", 0, BooleanField, "equals", "hello").is_valid
        assert not Filter("bob", 0, BooleanField, "pontains", "True").is_valid

    def test_default_lookup(self):
        assert BooleanField.default_lookup == "equals"


class TestCalculatedField:
    def test_validate(self):
        assert not Filter("bob", 0, CalculatedField, "gt", "1").is_valid
