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
    group = (
        {"fa": StringField, "fd": StringField, "fn": StringField, "bob": StringField},
        {"tom": ({"jones": StringField}, {"michael": ({"bolton": StringField}, {})})},
    )
    return BoundQuery(query, group)


@pytest.fixture
def filter(query):
    return Filter(0, StringField("bob", query), "equals", "fred")


class TestQuery:
    def test_from_request(self, query):
        q = Query.from_request(
            "app", "model", "+fa,-fd,fn", "html", {"bob__equals": ["fred"]}
        )
        assert q == query

    def test_from_request_with_related_filter(self, query):

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
    def test_csv_link(self, bound_query):
        assert (
            bound_query.csv_link
            == "/data_browser/query/app/model/+fa,-fd,fn.csv?bob__equals=fred"
        )

    def test_save_link(self, bound_query):
        assert (
            bound_query.save_link
            == "/admin/data_browser/view/add/?app=app&model=model&fields=%2Bfa%2C-fd%2Cfn&query=%7B%22bob__equals%22%3A+%5B%22fred%22%5D%7D"
        )

    def test_fields(self, query, bound_query):
        assert list(bound_query.fields) == ["fa", "fd", "fn"]

    def test_calculated_fields(self, query, bound_query):
        assert list(bound_query.calculated_fields) == []
        bound_query.all_fields["fa"].concrete = False
        assert list(bound_query.calculated_fields) == ["fa"]

    def test_sort_fields(self, query, bound_query):
        assert list(bound_query.sort_fields) == [
            (StringField("fa", query), ASC, "↓"),
            (StringField("fd", query), DSC, "↑"),
            (StringField("fn", query), None, ""),
        ]

    def test_filters(self, bound_query, filter):
        assert list(bound_query.filters) == [filter]

    def test_all_fields(self, query, bound_query):
        assert bound_query.all_fields == {
            "fa": StringField("fa", query),
            "fd": StringField("fd", query),
            "fn": StringField("fn", query),
            "bob": StringField("bob", query),
            "tom__jones": StringField("tom__jones", query),
            "tom__michael__bolton": StringField("tom__michael__bolton", query),
        }

    def test_all_nested(self, query, bound_query):
        assert bound_query.all_fields_nested == (
            {
                "fa": StringField("fa", query),
                "fd": StringField("fd", query),
                "fn": StringField("fn", query),
                "bob": StringField("bob", query),
            },
            {
                "tom": (
                    "tom",
                    (
                        {"jones": StringField("tom__jones", query)},
                        {
                            "michael": (
                                "tom__michael",
                                (
                                    {
                                        "bolton": StringField(
                                            "tom__michael__bolton", query
                                        )
                                    },
                                    {},
                                ),
                            )
                        },
                    ),
                )
            },
        )


class TestFilter:
    def test_url_name(self, filter):
        assert filter.url_name == "bob__equals"

    def test_remove_link(self, filter):
        assert filter.remove_link == "/data_browser/query/app/model/+fa,-fd,fn.html"

    def test_lookups(self, filter):
        expected = [
            (f, f"/data_browser/query/app/model/+fa,-fd,fn.html?bob__{f}=fred")
            for f in StringField.lookups
        ]
        assert list(filter.lookups) == expected


class TestField:
    def test_add_link(self, query):
        assert (
            StringField("bob", query).add_link
            == "/data_browser/query/app/model/+fa,-fd,fn,bob.html?bob__equals=fred"
        )

    def test_remove_link(self, query):
        assert (
            StringField("fd", query).remove_link
            == "/data_browser/query/app/model/+fa,fn.html?bob__equals=fred"
        )

    def test_add_filter_link(self, query):
        assert (
            StringField("fd", query).add_filter_link
            == "/data_browser/query/app/model/+fa,-fd,fn.html?bob__equals=fred&fd__equals="
        )

    def test_toggle_sort_link(self, query):
        assert (
            StringField("fa", query).toggle_sort_link
            == "/data_browser/query/app/model/-fa,-fd,fn.html?bob__equals=fred"
        )
        assert (
            StringField("fd", query).toggle_sort_link
            == "/data_browser/query/app/model/+fa,fd,fn.html?bob__equals=fred"
        )
        assert (
            StringField("fn", query).toggle_sort_link
            == "/data_browser/query/app/model/+fa,-fd,+fn.html?bob__equals=fred"
        )

    def test_repr(self, query):
        assert repr(StringField("fa", query)) == f"StringField('fa', {query})"


class TestStringField:
    def test_validate(self):
        assert not StringField(None, None).validate("contains", "hello")
        assert StringField(None, None).validate("pontains", "hello")


class TestNumberField:
    def test_validate(self):
        assert not NumberField(None, None).validate("gt", "6.1")
        assert NumberField(None, None).validate("pontains", "6.1")
        assert NumberField(None, None).validate("gt", "hello")
        assert not NumberField(None, None).validate("is_null", "True")
        assert NumberField(None, None).validate("is_null", "hello")


class TestTimeField:
    def test_validate(self):
        assert not TimeField(None, None).validate("gt", "2018-03-20T22:31:23")
        assert TimeField(None, None).validate("gt", "hello")
        assert TimeField(None, None).validate("pontains", "2018-03-20T22:31:23")
        assert not TimeField(None, None).validate("is_null", "True")
        assert TimeField(None, None).validate("is_null", "hello")


class TestBooleanField:
    def test_validate(self):
        assert not BooleanField(None, None).validate("equal", "True")
        assert BooleanField(None, None).validate("equal", "hello")
        assert BooleanField(None, None).validate("pontains", "True")


class TestCalculatedField:
    def test_validate(self):
        assert CalculatedField(None, None).validate("gt", "1")
