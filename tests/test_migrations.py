import pytest

from data_browser import migration_helpers
from data_browser.models import View
from data_browser.orm_admin import get_models
from data_browser.query import BoundQuery


@pytest.fixture
def models(req):
    return get_models(req)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "before,after",
    [
        # is_null
        ("name__is_null=True", "name__is_null=IsNull"),
        ("name__is_null=False", "name__is_null=NotNull"),
        ("name__is_null=true", "name__is_null=IsNull"),
        ("name__is_null=false", "name__is_null=NotNull"),
        # is_null equals
        ("name__is_null__equals=True", "name__is_null__equals=IsNull"),
        ("name__is_null__equals=False", "name__is_null__equals=NotNull"),
        ("name__is_null__equals=true", "name__is_null__equals=IsNull"),
        ("name__is_null__equals=false", "name__is_null__equals=NotNull"),
        # string_choice equals / not_equals
        ("string_choice__equals=a", "string_choice__equals=A"),
        ("string_choice__equals=c", "string_choice__raw__equals=c"),
        ("string_choice__not_equals=a", "string_choice__not_equals=A"),
        ("string_choice__not_equals=c", "string_choice__raw__not_equals=c"),
        # string_choice other
        ("string_choice__contains=a", "string_choice__raw__contains=a"),
        ("string_choice__starts_with=a", "string_choice__raw__starts_with=a"),
        ("string_choice__ends_with=a", "string_choice__raw__ends_with=a"),
        ("string_choice__regex=a", "string_choice__raw__regex=a"),
        ("string_choice__not_contains=a", "string_choice__raw__not_contains=a"),
        ("string_choice__not_starts_with=a", "string_choice__raw__not_starts_with=a"),
        ("string_choice__not_ends_with=a", "string_choice__raw__not_ends_with=a"),
        ("string_choice__not_regex=a", "string_choice__raw__not_regex=a"),
        # number_choice equals / not_equals
        ("number_choice__equals=1", "number_choice__equals=A"),
        ("number_choice__equals=3", "number_choice__raw__equals=3.0"),
        ("number_choice__not_equals=1", "number_choice__not_equals=A"),
        ("number_choice__not_equals=3", "number_choice__raw__not_equals=3.0"),
        # number_choice other
        ("number_choice__gt=1", "number_choice__raw__gt=1"),
        ("number_choice__gte=1", "number_choice__raw__gte=1"),
        ("number_choice__lt=1", "number_choice__raw__lt=1"),
        ("number_choice__lte=1", "number_choice__raw__lte=1"),
        # other good stuff
        ("name__equals=bob", "name__equals=bob"),
        ("name__contains=bob", "name__contains=bob"),
        ("boat__equals=1", "boat__equals=1"),
        ("boat__gt=1", "boat__gt=1"),
        # other bad stuff
        ("wtf__is_null=True", "wtf__is_null=True"),
        ("wtf__is_null__equals=True", "wtf__is_null__equals=True"),
        ("wtf__equals=a", "wtf__equals=a"),
        ("wtf__contains=bob", "wtf__contains=bob"),
        ("wtf__gt=1", "wtf__gt=1"),
        ("string_choice__wtf=a", "string_choice__raw__wtf=a"),
        ("number_choice__wtf=1", "number_choice__raw__wtf=1"),
        ("name__is_null=wtf", "name__is_null=wtf"),
        ("name__is_null__equals=wtf", "name__is_null__equals=wtf"),
    ],
)
def test_0009(models, before, after):
    valid = int("wtf" not in before)

    view = View.objects.create(model_name="core.Product", query=before)
    migration_helpers.forwards_0009(View)
    view.refresh_from_db()
    assert view.query == after
    assert len(BoundQuery.bind(view.get_query(), models).valid_filters) == valid

    view = View.objects.create(model_name="core.SKU", query=f"product__{before}")
    migration_helpers.forwards_0009(View)
    view.refresh_from_db()
    assert view.query == f"product__{after}"
    assert len(BoundQuery.bind(view.get_query(), models).valid_filters) == valid


def test_0009_multiple_filters(models):
    view = View.objects.create(
        model_name="core.Product",
        query="name__is_null=True&boat__gt=1&name__is_null__equals=True",
    )
    migration_helpers.forwards_0009(View)
    view.refresh_from_db()
    assert view.query == "name__is_null=IsNull&boat__gt=1&name__is_null__equals=IsNull"
    assert len(BoundQuery.bind(view.get_query(), models).valid_filters) == 3


@pytest.mark.django_db
def test_0009_no_filters():
    view = View.objects.create(model_name="core.Product")
    migration_helpers.forwards_0009(View)
    view.refresh_from_db()
    assert view.query == ""
