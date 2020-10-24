import pytest
from django.contrib import admin

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
@pytest.mark.usefixtures("db")
def get_results_flat(req):  # pragma: postgres
    def helper(fields, query=None):
        query = query or {}

        admin.site.register(ArrayModel, ArrayAdmin)
        try:
            orm_models = get_models(req)
            query = Query.from_request("array.ArrayModel", fields, query)
            bound_query = BoundQuery.bind(query, orm_models)
            data = get_results(req, bound_query, orm_models, False)
        finally:
            admin.site.unregister(ArrayModel)
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
            "int_array_field": "1, 2",
            "char_array_field": "a, b",
            "int_choice_array_field": "A, B",
            "char_choice_array_field": "A, B",
        }
    ]


def test_filter_contains(get_results_flat):  # pragma: postgres
    ArrayModel.objects.create(int_array_field=[1, 2])
    ArrayModel.objects.create(int_array_field=[2, 3])
    ArrayModel.objects.create(int_array_field=[3, 4])
    assert get_results_flat("int_array_field", {"int_array_field__contains": [2]}) == [
        {"int_array_field": "1, 2"},
        {"int_array_field": "2, 3"},
    ]


def test_filter_length(get_results_flat):  # pragma: postgres
    ArrayModel.objects.create(int_array_field=[1])
    ArrayModel.objects.create(int_array_field=[1, 2])
    ArrayModel.objects.create(int_array_field=[1, 2, 3])
    assert get_results_flat("int_array_field", {"int_array_field__length": [2]}) == [
        {"int_array_field": "1, 2"}
    ]
