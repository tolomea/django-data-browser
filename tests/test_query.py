import pytest
from data_browser.query import (
    ASC,
    DSC,
    BooleanField,
    BoundQuery,
    CalculatedField,
    Field,
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
        {"fa": Field, "fd": Field, "fn": Field, "bob": Field},
        {"tom": ({"jones": Field}, {"michael": ({"bolton": Field}, {})})},
    )
    return BoundQuery(query, group)


@pytest.fixture
def filter(query):
    return Filter(0, Field("bob", query), "equals", "fred")


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
            (Field("fa", query), ASC, "↓"),
            (Field("fd", query), DSC, "↑"),
            (Field("fn", query), None, ""),
        ]

    def test_filters(self, bound_query, filter):
        assert list(bound_query.filters) == [filter]

    def test_all_fields(self, query, bound_query):
        assert bound_query.all_fields == {
            "fa": Field("fa", query),
            "fd": Field("fd", query),
            "fn": Field("fn", query),
            "bob": Field("bob", query),
            "tom__jones": Field("tom__jones", query),
            "tom__michael__bolton": Field("tom__michael__bolton", query),
        }

    def test_all_nested(self, query, bound_query):
        assert bound_query.all_fields_nested == (
            {
                "fa": Field("fa", query),
                "fd": Field("fd", query),
                "fn": Field("fn", query),
                "bob": Field("bob", query),
            },
            {
                "tom": (
                    "tom",
                    (
                        {"jones": Field("tom__jones", query)},
                        {
                            "michael": (
                                "tom__michael",
                                ({"bolton": Field("tom__michael__bolton", query)}, {}),
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
        assert list(filter.lookups) == [
            (
                "equals",
                "/data_browser/query/app/model/+fa,-fd,fn.html?bob__equals=fred",
            ),
            (
                "not_equals",
                "/data_browser/query/app/model/+fa,-fd,fn.html?bob__not_equals=fred",
            ),
            (
                "is_null",
                "/data_browser/query/app/model/+fa,-fd,fn.html?bob__is_null=fred",
            ),
        ]


class TestField:
    def test_add_link(self, query):
        assert (
            Field("bob", query).add_link
            == "/data_browser/query/app/model/+fa,-fd,fn,bob.html?bob__equals=fred"
        )

    def test_remove_link(self, query):
        assert (
            Field("fd", query).remove_link
            == "/data_browser/query/app/model/+fa,fn.html?bob__equals=fred"
        )

    def test_add_filter_link(self, query):
        assert (
            Field("fd", query).add_filter_link
            == "/data_browser/query/app/model/+fa,-fd,fn.html?bob__equals=fred&fd__equals="
        )

    def test_toggle_sort_link(self, query):
        assert (
            Field("fa", query).toggle_sort_link
            == "/data_browser/query/app/model/-fa,-fd,fn.html?bob__equals=fred"
        )
        assert (
            Field("fd", query).toggle_sort_link
            == "/data_browser/query/app/model/+fa,fd,fn.html?bob__equals=fred"
        )
        assert (
            Field("fn", query).toggle_sort_link
            == "/data_browser/query/app/model/+fa,-fd,+fn.html?bob__equals=fred"
        )

    def test_repr(self, query):
        assert repr(Field("fa", query)) == f"Field('fa', {query})"


class TestStringField:
    def test_is_valid(self):
        assert StringField(None, None).is_valid("contains", "hello")
        assert not StringField(None, None).is_valid("pontains", "hello")


class TestNumberField:
    def test_is_valid(self):
        assert NumberField(None, None).is_valid("gt", "6.1")
        assert not NumberField(None, None).is_valid("pontains", "6.1")
        assert not NumberField(None, None).is_valid("gt", "hello")
        assert NumberField(None, None).is_valid("is_null", "True")
        assert not NumberField(None, None).is_valid("is_null", "hello")


class TestTimeField:
    def test_is_valid(self):
        assert TimeField(None, None).is_valid("gt", "2018-03-20T22:31:23")
        assert not TimeField(None, None).is_valid("gt", "hello")
        assert not TimeField(None, None).is_valid("pontains", "2018-03-20T22:31:23")
        assert TimeField(None, None).is_valid("is_null", "True")
        assert not TimeField(None, None).is_valid("is_null", "hello")


class TestBooleanField:
    def test_is_valid(self):
        assert BooleanField(None, None).is_valid("is_null", "True")
        assert not BooleanField(None, None).is_valid("is_null", "hello")
        assert not BooleanField(None, None).is_valid("pontains", "True")


class TestCalculatedField:
    def test_is_valid(self):
        assert not CalculatedField(None, None).is_valid("gt", "1")
