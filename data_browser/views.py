import csv
import io
import json
from collections import defaultdict

import django.contrib.admin.views.decorators as admin_decorators
import requests
from django import http
from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.db import models
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.forms.models import _get_foreign_key
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template import engines, loader
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import View
from .query import (
    ASC,
    DSC,
    TYPES,
    BooleanFieldType,
    BoundQuery,
    CalculatedFieldType,
    NumberFieldType,
    Query,
    StringFieldType,
    TimeFieldType,
)


def get_model(app, model):
    return apps.get_model(app_label=app, model_name=model)


FIELD_MAP = [
    ((models.BooleanField, models.NullBooleanField), BooleanFieldType),
    (
        (
            models.CharField,
            models.TextField,
            models.GenericIPAddressField,
            models.UUIDField,
        ),
        StringFieldType,
    ),
    ((models.DateTimeField, models.DateField), TimeFieldType),
    (
        (models.DecimalField, models.FloatField, models.IntegerField, models.AutoField),
        NumberFieldType,
    ),
    ((type(None),), CalculatedFieldType),
    ((models.FileField,), None),
]


def get_all_admin_fields(request):
    def from_fieldsets(admin, model):
        obj = model()  # we want the admin change field sets, not the add ones
        for f in flatten_fieldsets(admin.get_fieldsets(request, obj)):
            if hasattr(model, f):
                yield f

    all_admin_fields = defaultdict(set)
    for model, modeladmin in admin.site._registry.items():
        all_admin_fields[model].update(from_fieldsets(modeladmin, model))
        for inline in modeladmin.get_inline_instances(request):
            all_admin_fields[inline.model].update(from_fieldsets(inline, inline.model))
            all_admin_fields[inline.model].add(
                _get_foreign_key(model, inline.model, inline.fk_name).name
            )
    # we always have pk
    for fields in all_admin_fields.values():
        if fields:
            fields.add("pk")
    return all_admin_fields


def get_fields_for_model(model, admin_fields):
    # {"fields": {field_name, FieldType}, "fks": {field_name: model}}
    fields = {}
    fks = {}

    model_fields = {f.name: f for f in model._meta.get_fields()}
    if "id" in model_fields:
        model_fields["pk"] = model_fields["id"]

    for field_name in admin_fields[model]:
        field = model_fields.get(field_name)
        if not isinstance(field, (ForeignObjectRel, models.ManyToManyField)):
            if isinstance(field, models.ForeignKey):
                fks[field_name] = field.related_model
            else:
                for django_types, field_type in FIELD_MAP:
                    if isinstance(field, django_types):
                        if field_type:
                            fields[field_name] = field_type
                        break
                else:  # pragma: no cover
                    print(
                        f"DataBrowser: {model.__name__}.{field_name} unknown type {type(field).__name__}"
                    )
    return {"fields": fields, "fks": fks}


def get_all_model_fields(admin_fields):
    # {model: {"fields": {field_name, FieldType}, "fks": {field_name: model}}}
    return {model: get_fields_for_model(model, admin_fields) for model in admin_fields}


def get_django_lookup(field_type, lookup):
    if field_type == StringFieldType and lookup == "equals":
        return "iexact"
    else:
        lookup = {
            "equals": "exact",
            "regex": "iregex",
            "contains": "icontains",
            "starts_with": "istartswith",
            "ends_with": "iendswith",
            "is_null": "isnull",
            "gt": "gt",
            "gte": "gte",
            "lt": "lt",
            "lte": "lte",
        }[lookup]
        return lookup


def get_data(bound_query):
    if not bound_query.fields:
        return []

    qs = get_model(bound_query.app, bound_query.model).objects.all()

    # sort
    sort_fields = []
    for name, field, sort_direction in bound_query.sort_fields:
        if name not in bound_query.calculated_fields:
            if sort_direction is ASC:
                sort_fields.append(name)
            if sort_direction is DSC:
                sort_fields.append(f"-{name}")
    qs = qs.order_by(*sort_fields)

    # filter
    for filter_ in bound_query.filters:
        if filter_.is_valid:
            negation = False

            lookup = filter_.lookup
            if lookup.startswith("not_"):
                negation = True
                lookup = lookup[4:]

            filter_str = f"{filter_.name}__{get_django_lookup(filter_.field, lookup)}"
            if negation:
                qs = qs.exclude(**{filter_str: filter_.parsed})
            else:
                qs = qs.filter(**{filter_str: filter_.parsed})

    # no calculated fields early out using qs.values
    if not bound_query.calculated_fields:
        data = []
        for row in qs.values(*bound_query.fields).distinct():
            data.append([t.format(row[f]) for f, t in bound_query.fields.items()])
        return data

    # preloading
    select_related = set()

    def add_select_relateds(name):
        while "__" in name:
            name = name.rsplit("__", 1)[0]
            select_related.add(name)

    for name, field, sort_direction in bound_query.sort_fields:
        if sort_direction is not None:
            add_select_relateds(name)

    for filter_ in bound_query.filters:
        if filter_.is_valid:
            add_select_relateds(filter_.name)

    prefetch_related = set()
    for field in bound_query.fields:
        if "__" in field:
            prefetch_related.add(field.rsplit("__", 1)[0])
    prefetch_related -= select_related

    if select_related:
        qs = qs.select_related(*select_related)
    if prefetch_related:
        qs = qs.prefetch_related(*prefetch_related)

    # get data
    def lookup(obj, name):
        value = obj
        for part in name.split("__"):
            value = getattr(value, part, None)
        return value() if callable(value) else value

    data = []
    for row in qs.distinct():
        data.append([t.format(lookup(row, f)) for f, t in bound_query.fields.items()])
    return data


def get_context(request, base_model):
    admin_fields = get_all_admin_fields(request)
    all_model_fields = get_all_model_fields(admin_fields)

    types = {
        name: {
            "lookups": {n: {"type": t} for n, t in type_.lookups.items()},
            "sorted_lookups": list(type_.lookups),
            "defaultLookup": type_.default_lookup,
            "defaultValue": type_.default_value,
        }
        for name, type_ in TYPES.items()
    }

    def model_name(model):
        return f"{model._meta.app_label}.{model.__name__}"

    front_fields = ["pk"]
    all_model_fields = {
        model_name(model): {
            "fields": {
                name: {"type": type_.name, "concrete": type_.concrete}
                for name, type_ in model_fields["fields"].items()
            },
            "fks": {
                name: {"model": model_name(rel_model)}
                for name, rel_model in model_fields["fks"].items()
            },
            "sorted_fields": front_fields
            + sorted(f for f in model_fields["fields"] if f not in front_fields),
            "sorted_fks": sorted(model_fields["fks"]),
        }
        for model, model_fields in all_model_fields.items()
    }

    return {
        "model": model_name(base_model),
        "baseUrl": reverse("data_browser:root"),
        "adminUrl": reverse(f"admin:{View._meta.db_table}_add"),
        "types": types,
        "fields": all_model_fields,
    }


@admin_decorators.staff_member_required
def query_ctx(request, *, app, model, fields=""):  # pragma: no cover
    try:
        model = get_model(app, model)
    except LookupError as e:
        return HttpResponse(e)
    return JsonResponse(get_context(request, model))


@admin_decorators.staff_member_required
def query_html(request, *, app, model, fields=""):
    try:
        model = get_model(app, model)
    except LookupError as e:
        return HttpResponse(e)

    data = get_context(request, model)
    data = json.dumps(data)
    data = data.replace("<", "\\u003C").replace(">", "\\u003E").replace("&", "\\u0026")

    if getattr(settings, "DATA_BROWSER_DEV", False):  # pragma: no cover
        response = _get_from_js_dev_server(request)
        template = engines["django"].from_string(response.text)
    else:
        template = loader.get_template("data_browser/index.html")

    return TemplateResponse(request, template, {"data": data})


@admin_decorators.staff_member_required
def query(request, *, app, model, fields="", media):
    query = Query.from_request(app, model, fields, media, request.GET)
    if media == "csv":
        return csv_response(request, query)
    elif media == "json":
        return json_response(request, query)
    else:
        assert False


def csv_response(request, query):
    admin_fields = get_all_admin_fields(request)
    all_model_fields = get_all_model_fields(admin_fields)
    bound_query = BoundQuery(query, get_model(query.app, query.model), all_model_fields)
    data = get_data(bound_query)

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(bound_query.fields)
    writer.writerows(data)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type="text/csv")
    response[
        "Content-Disposition"
    ] = f"attachment; filename={query.model}-{timezone.now().isoformat()}.csv"
    return response


def json_response(request, query):
    admin_fields = get_all_admin_fields(request)
    all_model_fields = get_all_model_fields(admin_fields)
    bound_query = BoundQuery(query, get_model(query.app, query.model), all_model_fields)
    data = get_data(bound_query)

    return JsonResponse(
        {
            "data": data,
            "filters": [
                {
                    "errorMessage": filter_.err_message,
                    "name": filter_.name,
                    "lookup": filter_.lookup,
                    "value": filter_.value,
                }
                for filter_ in bound_query.filters
            ],
            "fields": [
                {"name": name, "sort": sort_direction}
                for (name, field, sort_direction) in bound_query.sort_fields
            ],
        }
    )


def view(request, pk, media):
    view = get_object_or_404(View.objects.filter(public=True), pk=pk)
    request.user = view.owner  # public views are run as the person who created them
    query = view.get_query(media)

    if media == "csv":
        return csv_response(request, query)
    elif media == "json":
        return json_response(request, query)
    else:
        assert False


def _get_from_js_dev_server(request):  # pragma: no cover
    upstream_url = f"http://localhost:3000{request.path}"
    method = request.META["REQUEST_METHOD"].lower()
    return getattr(requests, method)(upstream_url, stream=True)


@csrf_exempt
def proxy_js_dev_server(request, path):  # pragma: no cover
    """
    Proxy HTTP requests to the frontend dev server in development.

    The implementation is very basic e.g. it doesn't handle HTTP headers.

    """
    response = _get_from_js_dev_server(request)
    content_type = response.headers.get("Content-Type")

    if request.META.get("HTTP_UPGRADE", "").lower() == "websocket":
        return http.HttpResponse(
            content="WebSocket connections aren't supported",
            status=501,
            reason="Not Implemented",
        )

    else:
        return http.StreamingHttpResponse(
            streaming_content=response.iter_content(2 ** 12),
            content_type=content_type,
            status=response.status_code,
            reason=response.reason,
        )
