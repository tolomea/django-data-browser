import pytest
from django.contrib import admin

from data_browser import migration_helpers
from data_browser.models import View
from data_browser.orm_admin import get_models
from data_browser.orm_results import get_results
from data_browser.query import BoundQuery, Query

from .conftest import ARRAY_FIELD_SUPPORT

if ARRAY_FIELD_SUPPORT:  # pragma: postgres
    from .array.models import ArrayModel
else:  # pragma: not postgres
    pytestmark = pytest.mark.skip("Needs ArrayField support")


class ArrayAdmin(admin.ModelAdmin):
    fields = [
        "char_array_field",
        "int_array_field",
        "char_choice_array_field",
        "int_choice_array_field",
    ]


@pytest.fixture
def with_arrays(db):  # pragma: postgres
    admin.site.register(ArrayModel, ArrayAdmin)
    yield
    admin.site.unregister(ArrayModel)


@pytest.fixture
def get_results_flat(with_arrays, req):  # pragma: postgres
    def helper(fields, query=None):
        query = query or []

        orm_models = get_models(req)
        query = Query.from_request("array.ArrayModel", fields, query)
        bound_query = BoundQuery.bind(query, orm_models)
        data = get_results(req, bound_query, orm_models, False)

        for f in bound_query.filters:
            if f.err_message:
                print(
                    "filter error:", f.path_str, f.lookup, f.value, "->", f.err_message
                )

        return data["rows"]

    return helper


def test_hello_world(get_results_flat):  # pragma: postgres
    ArrayModel.objects.create(
        int_array_field=[1, 2],
        char_array_field=["a", "b"],
        int_choice_array_field=[1, 2],
        char_choice_array_field=["a", "b"],
    )
    assert get_results_flat(
        "int_array_field,char_array_field,int_choice_array_field,char_choice_array_field"
    ) == [
        {
            "int_array_field": "[1.0, 2.0]",
            "char_array_field": '["a", "b"]',
            "int_choice_array_field": '["A", "B"]',
            "char_choice_array_field": '["A", "B"]',
        }
    ]


def test_int_array_contains(get_results_flat):  # pragma: postgres
    ArrayModel.objects.create(int_array_field=[1, 2])
    ArrayModel.objects.create(int_array_field=[2, 3])
    ArrayModel.objects.create(int_array_field=[1, 3])
    assert get_results_flat(
        "int_array_field", [("int_array_field__contains", "2")]
    ) == [
        {"int_array_field": "[1.0, 2.0]"},
        {"int_array_field": "[2.0, 3.0]"},
    ]


def test_int_choice_array_contains(get_results_flat):  # pragma: postgres
    ArrayModel.objects.create(int_choice_array_field=[1, 2])
    ArrayModel.objects.create(int_choice_array_field=[2, 3])
    ArrayModel.objects.create(int_choice_array_field=[1, 3])
    assert get_results_flat(
        "int_choice_array_field", [("int_choice_array_field__contains", "B")]
    ) == [
        {"int_choice_array_field": '["A", "B"]'},
        {"int_choice_array_field": '["B", "C"]'},
    ]


def test_char_array_contains(get_results_flat):  # pragma: postgres
    ArrayModel.objects.create(char_array_field=["a", "b"])
    ArrayModel.objects.create(char_array_field=["b", "c"])
    ArrayModel.objects.create(char_array_field=["a", "c"])
    assert get_results_flat(
        "char_array_field", [("char_array_field__contains", "b")]
    ) == [{"char_array_field": '["a", "b"]'}, {"char_array_field": '["b", "c"]'}]


def test_char_choice_array_contains(get_results_flat):  # pragma: postgres
    ArrayModel.objects.create(char_choice_array_field=["a", "b"])
    ArrayModel.objects.create(char_choice_array_field=["b", "c"])
    ArrayModel.objects.create(char_choice_array_field=["a", "c"])
    assert get_results_flat(
        "char_choice_array_field", [("char_choice_array_field__contains", "B")]
    ) == [
        {"char_choice_array_field": '["A", "B"]'},
        {"char_choice_array_field": '["B", "C"]'},
    ]


def test_filter_length(get_results_flat):  # pragma: postgres
    ArrayModel.objects.create(int_array_field=[1])
    ArrayModel.objects.create(int_array_field=[1, 2])
    ArrayModel.objects.create(int_array_field=[1, 2, 3])
    assert get_results_flat("int_array_field", [("int_array_field__length", "2")]) == [
        {"int_array_field": "[1.0, 2.0]"}
    ]


def test_choice_array_filter_length(get_results_flat):  # pragma: postgres
    ArrayModel.objects.create(int_choice_array_field=[1])
    ArrayModel.objects.create(int_choice_array_field=[1, 2])
    ArrayModel.objects.create(int_choice_array_field=[1, 2, 3])
    assert get_results_flat(
        "int_choice_array_field", [("int_choice_array_field__length", "2")]
    ) == [{"int_choice_array_field": '["A", "B"]'}]


def test_char_choice_array_equals(get_results_flat):  # pragma: postgres
    ArrayModel.objects.create(char_choice_array_field=["a", "b"])
    ArrayModel.objects.create(char_choice_array_field=["b", "c"])
    ArrayModel.objects.create(char_choice_array_field=["a", "c"])
    assert get_results_flat(
        "char_choice_array_field", [("char_choice_array_field__equals", '["A", "B"]')]
    ) == [{"char_choice_array_field": '["A", "B"]'}]


@pytest.mark.parametrize(
    "before,after",
    [
        # choice_array contains / not_contains
        ("char_choice_array_field__contains=a", "char_choice_array_field__contains=A"),
        (
            "char_choice_array_field__contains=d",
            "char_choice_array_field__raw__contains=d",
        ),
        ("int_choice_array_field__contains=1", "int_choice_array_field__contains=A"),
        (
            "int_choice_array_field__contains=4",
            "int_choice_array_field__raw__contains=4.0",
        ),
        # choice_array other -> noop
        ("char_choice_array_field__length=1", "char_choice_array_field__length=1"),
        ("int_choice_array_field__length=1", "int_choice_array_field__length=1"),
        ("char_choice_array_field__wtf=1", "char_choice_array_field__wtf=1"),
        ("int_choice_array_field__wtf=1", "int_choice_array_field__wtf=1"),
        # regular array -> noop
        ("char_array_field__contains=a", "char_array_field__contains=a"),
        ("int_array_field__contains=1", "int_array_field__contains=1"),
    ],
)
def test_0009(req, with_arrays, before, after):  # pragma: postgres
    orm_models = get_models(req)
    valid = int("wtf" not in before)

    view = View.objects.create(model_name="array.ArrayModel", query=before)
    migration_helpers.forwards_0009(View)
    view.refresh_from_db()
    assert view.query == after
    assert len(BoundQuery.bind(view.get_query(), orm_models).valid_filters) == valid
