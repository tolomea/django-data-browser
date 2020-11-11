import pytest
from django.contrib import admin

from data_browser.helpers import AdminMixin
from data_browser.orm_admin import get_models
from data_browser.orm_results import get_results
from data_browser.query import BoundQuery, Query

from .conftest import JSON_FIELD_SUPPORT

""" Howto enable SQLite JSON support https://code.djangoproject.com/wiki/JSON1Extension """


if JSON_FIELD_SUPPORT:
    from .json.models import JsonModel
else:  # pragma: no cover
    pytestmark = pytest.mark.skip("Needs JSONField support")


class JsonAdmin(AdminMixin, admin.ModelAdmin):
    fields = ["json_field"]
    ddb_json_fields = {"json_field": {"hello": "string"}}


@pytest.fixture
def with_json(db):
    admin.site.register(JsonModel, JsonAdmin)
    yield
    admin.site.unregister(JsonModel)


@pytest.fixture
def get_results_flat(with_json, req):
    def helper(fields, query=None):
        query = query or {}

        orm_models = get_models(req)
        query = Query.from_request("json.JsonModel", fields, query)
        bound_query = BoundQuery.bind(query, orm_models)
        data = get_results(req, bound_query, orm_models, False)

        for f in bound_query.filters:
            if f.err_message:
                print(
                    "filter error:", f.path_str, f.lookup, f.value, "->", f.err_message
                )

        return data["rows"]

    return helper


def test_hello_world(get_results_flat):
    JsonModel.objects.create(json_field={"hello": "world"})
    assert get_results_flat("json_field") == [{"json_field": '{"hello": "world"}'}]


def test_get_sub_field(get_results_flat):
    JsonModel.objects.create(json_field={"hello": "world"})
    assert get_results_flat("json_field__hello") == [{"json_field__hello": "world"}]


def test_filter_sub_field(get_results_flat):
    JsonModel.objects.create(json_field={"hello": "world"})
    JsonModel.objects.create(json_field={"hello": "universe"})
    assert get_results_flat("json_field", {"json_field__hello__equals": ["world"]}) == [
        {"json_field": '{"hello": "world"}'}
    ]


def test_filter_field_value(get_results_flat):
    JsonModel.objects.create(json_field={"goodbye": "universe"})
    assert get_results_flat("json_field") == [{"json_field": '{"goodbye": "universe"}'}]
    assert (
        get_results_flat(
            "json_field", {"json_field__field_equals": ['goodbye|"world"']}
        )
        == []
    )


def test_filter_field_value_no_seperator(get_results_flat):
    JsonModel.objects.create(json_field={"goodbye": "universe"})
    assert get_results_flat(
        "json_field", {"json_field__field_equals": ['goodbye"world"']}
    ) == [{"json_field": '{"goodbye": "universe"}'}]


def test_filter_field_value_no_field(get_results_flat):
    JsonModel.objects.create(json_field={"goodbye": "universe"})
    assert get_results_flat(
        "json_field", {"json_field__field_equals": ['|"world"']}
    ) == [{"json_field": '{"goodbye": "universe"}'}]


def test_filter_field_value_list(get_results_flat):
    JsonModel.objects.create(json_field={"goodbye": ["world"]})
    JsonModel.objects.create(json_field={"goodbye": ["universe"]})
    assert get_results_flat(
        "json_field", {"json_field__field_equals": ['goodbye|["world"]']}
    ) == [{"json_field": '{"goodbye": ["world"]}'}]


def test_filter_field_value_bad_json(get_results_flat):
    JsonModel.objects.create(json_field={"goodbye": "universe"})
    assert get_results_flat(
        "json_field", {"json_field__field_equals": ["goodbye|world"]}
    ) == [{"json_field": '{"goodbye": "universe"}'}]


def test_filter_has_key(get_results_flat):
    JsonModel.objects.create(json_field={"hello": "world"})
    JsonModel.objects.create(json_field={"goodbye": "world"})
    assert get_results_flat("json_field", {"json_field__has_key": ["hello"]}) == [
        {"json_field": '{"hello": "world"}'}
    ]


def test_filter_equals(get_results_flat):
    JsonModel.objects.create(json_field={"hello": "world"})
    JsonModel.objects.create(json_field={"goodbye": "world"})
    assert get_results_flat(
        "json_field", {"json_field__equals": ['{"hello": "world"}']}
    ) == [{"json_field": '{"hello": "world"}'}]


def test_filter_equals_bad_json(get_results_flat):
    JsonModel.objects.create(json_field={"hello": "world"})
    JsonModel.objects.create(json_field={"goodbye": "world"})
    assert get_results_flat(
        "json_field-1", {"json_field__equals": ['{"hello": "world"']}
    ) == [{"json_field": '{"hello": "world"}'}, {"json_field": '{"goodbye": "world"}'}]
