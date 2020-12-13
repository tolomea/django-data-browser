from urllib.parse import parse_qsl, urlencode

from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.urls import reverse

from data_browser.orm_admin import get_models
from data_browser.types import (
    IsNullType,
    NumberChoiceArrayType,
    NumberChoiceType,
    StringChoiceArrayType,
    StringChoiceType,
)


def _fix_filter(models, field, parts, lookup, value):
    if lookup == "is_null":
        value = {"true": "IsNull", "false": "NotNull"}.get(value.lower(), value)
    elif field.type_ == IsNullType and lookup == "equals":
        value = {"true": "IsNull", "false": "NotNull"}.get(value.lower(), value)
    elif field.type_ in [StringChoiceType, NumberChoiceType]:
        if lookup in ["equals", "not_equals"]:
            value, err = field.type_.raw_type.parse_lookup(lookup, value, None)
            choices = dict(field.choices)
            if err is None and value in choices:
                value = choices[value]
            else:
                parts.append("raw")
        elif lookup == "is_null":
            assert False  # should have been caught above
        else:
            parts.append("raw")
    elif field.type_ in [
        StringChoiceArrayType,
        NumberChoiceArrayType,
    ]:  # pragma: postgres
        if lookup in ["contains", "not_contains"]:
            value, err = field.type_.raw_type.parse_lookup(lookup, value, None)
            choices = dict(field.choices)
            if err is None and value in choices:
                value = choices[value]
            else:
                parts.append("raw")
    else:
        pass

    return parts, lookup, value


def forwards_0009(View):
    User = get_user_model()

    request = RequestFactory().get(reverse("admin:index"))
    request.user = User(is_superuser=True)
    models = get_models(request)

    for view in View.objects.all():
        filters = []
        for key, value in parse_qsl(view.query):
            *parts, lookup = key.split("__")

            model_name = view.model_name
            for part in parts:
                model = models[model_name]
                if part not in model.fields:
                    break
                field = model.fields[part]
                model_name = field.rel_name
            else:
                parts, lookup, value = _fix_filter(models, field, parts, lookup, value)

            key = "__".join(parts + [lookup])
            filters.append((key, value))
        view.query = urlencode(filters)
        view.save()
