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
            == "/data_browser/query/app/model/+fa,-fd,fn.html?bob__equals=fred"
        )


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
        assert not StringField.validate("contains", "hello")
        assert StringField.validate("pontains", "hello")

    def test_default_lookup(self):
        assert StringField.default_lookup == "equals"


class TestNumberField:
    def test_validate(self):
        assert not NumberField.validate("gt", "6.1")
        assert NumberField.validate("pontains", "6.1")
        assert NumberField.validate("gt", "hello")
        assert not NumberField.validate("is_null", "True")
        assert NumberField.validate("is_null", "hello")

    def test_default_lookup(self):
        assert NumberField.default_lookup == "equal"


class TestTimeField:
    def test_validate(self):
        assert not TimeField.validate("gt", "2018-03-20T22:31:23")
        assert TimeField.validate("gt", "hello")
        assert TimeField.validate("pontains", "2018-03-20T22:31:23")
        assert not TimeField.validate("is_null", "True")
        assert TimeField.validate("is_null", "hello")

    def test_default_lookup(self):
        assert TimeField.default_lookup == "equal"


class TestBooleanField:
    def test_validate(self):
        assert not BooleanField.validate("equal", "True")
        assert BooleanField.validate("equal", "hello")
        assert BooleanField.validate("pontains", "True")

    def test_default_lookup(self):
        assert BooleanField.default_lookup == "equal"


class TestCalculatedField:
    def test_validate(self):
        assert CalculatedField.validate("gt", "1")
