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
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import engines, loader
from django.template.response import TemplateResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import View
from .query import (
    ASC,
    DSC,
    BooleanField,
    BoundQuery,
    CalculatedField,
    NumberField,
    Query,
    StringField,
    TimeField,
)


def get_model(query):
    return apps.get_model(app_label=query.app, model_name=query.model)


FIELD_MAP = [
    ((models.BooleanField, models.NullBooleanField), BooleanField),
    ((models.CharField, models.TextField), StringField),
    ((models.DateTimeField, models.DateField), TimeField),
    (
        (models.DecimalField, models.FloatField, models.IntegerField, models.AutoField),
        NumberField,
    ),
    ((type(None)), CalculatedField),
]


def get_all_admin_fields(request):
    def from_fieldsets(admin, model):
        for f in flatten_fieldsets(admin.get_fieldsets(request)):
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
    return all_admin_fields


def get_fields_for_model(model, admin_fields):
    # {"fields": {field_name, Field}, "fks": {field_name: model}}
    fields = {}
    fks = {}

    model_fields = {f.name: f for f in model._meta.get_fields()}
    model_fields["pk"] = model_fields["id"]

    for field_name in admin_fields[model]:
        field = model_fields.get(field_name)
        if not isinstance(field, (ForeignObjectRel, models.ManyToManyField)):
            if isinstance(field, models.ForeignKey):
                fks[field_name] = field.related_model
            else:
                for django_types, field_type in FIELD_MAP:
                    if isinstance(field, django_types):
                        fields[field_name] = field_type
                        break
                else:
                    assert isinstance(field, models.fields.files.FileField), type(field)
    return {"fields": fields, "fks": fks}


def get_nested_fields_for_model(model, admin_fields, seen=()):
    # res = {field_name: Field}, {field_name: res}
    data = get_fields_for_model(model, admin_fields)

    groups = {}
    for field_name, related_model in data["fks"].items():
        if related_model not in seen:
            group_fileds = get_nested_fields_for_model(
                related_model, admin_fields, seen + (model,)
            )
            groups[field_name] = group_fileds
    return data["fields"], groups


LOOKUP_MAP = {
    "equals": "__iexact",
    "equal": "",
    "regex": "__iregex",
    "contains": "__icontains",
    "starts_with": "__istartswith",
    "ends_with": "__iendswith",
    "is_null": "__isnull",
    "gt": "__gt",
    "gte": "__gte",
    "lt": "__lt",
    "lte": "__lte",
}


def get_data(bound_query):
    if not bound_query.fields:
        return []

    model = get_model(bound_query)

    calculated_fields = bound_query.calculated_fields

    sort_fields = []
    for field, sort_direction, sort_symbol in bound_query.sort_fields:
        if field.name not in calculated_fields:
            if sort_direction is ASC:
                sort_fields.append(field.name)
            if sort_direction is DSC:
                sort_fields.append(f"-{field.name}")
    qs = model.objects.order_by(*sort_fields)

    if not calculated_fields:
        qs = qs.values(*bound_query.fields)

    for filter_ in bound_query.filters:
        if filter_.is_valid:
            negation = False

            lookup = filter_.lookup
            if lookup.startswith("not_"):
                negation = True
                lookup = lookup[4:]

            filter_str = f"{filter_.name}{LOOKUP_MAP[lookup]}"
            if negation:
                qs = qs.exclude(**{filter_str: filter_.value})
            else:
                qs = qs.filter(**{filter_str: filter_.value})

    data = []

    for row in qs.distinct():
        if calculated_fields:

            def lookup(obj, name):
                value = getattr(row, name, None)
                return value() if callable(value) else value

            data.append([lookup(row, f) for f in bound_query.fields])
        else:
            data.append([row[f] for f in bound_query.fields])

    return data


@admin_decorators.staff_member_required
def query_html(request, *, app, model, fields=""):
    query = Query.from_request(app, model, fields, "html", request.GET)

    try:
        model = get_model(query)
    except LookupError as e:
        return HttpResponse(e)

    admin_fields = get_all_admin_fields(request)
    fields = get_nested_fields_for_model(model, admin_fields)
    bound_query = BoundQuery(query, fields)
    data = get_data(bound_query)

    def fmt_fields(fields, fks):
        return {
            "fields": [
                {
                    "name": name,
                    "concrete": field.concrete,
                    "add_filter_link": field.add_filter_link,
                    "add_link": field.add_link,
                }
                for name, field in sorted(fields.items())
            ],
            "fks": [
                {"name": name, "path": path, **fmt_fields(*child)}
                for name, (path, child) in sorted(fks.items())
            ],
        }

    data = {
        "query": {
            "model": bound_query.model,
            "base_url": bound_query.base_url,
            "csv_link": bound_query.csv_link,
            "save_link": bound_query.save_link,
            "filters": [
                {
                    "is_valid": filter_.is_valid,
                    "err_message": filter_.err_message,
                    "remove_link": filter_.remove_link,
                    "name": filter_.name,
                    "lookup": filter_.lookup,
                    "url_name": filter_.url_name,
                    "value": filter_.value,
                    "lookups": [
                        {"name": lookup.name, "link": lookup.link}
                        for lookup in filter_.lookups
                    ],
                }
                for filter_ in bound_query.filters
            ],
            "sort_fields": [
                {
                    "field": {
                        "remove_link": field.remove_link,
                        "concrete": field.concrete,
                        "add_filter_link": field.add_filter_link,
                        "toggle_sort_link": field.toggle_sort_link,
                        "name": field.name,
                    },
                    "sort_icon": sort_icon,
                }
                for (field, sort_direction, sort_icon) in bound_query.sort_fields
            ],
            "all_fields_nested": fmt_fields(*bound_query.all_fields_nested),
        },
        "data": data,
    }

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
    assert media == "csv"
    return csv_response(request, query)


def csv_response(request, query):
    admin_fields = get_all_admin_fields(request)
    fields = get_nested_fields_for_model(get_model(query), admin_fields)
    bound_query = BoundQuery(query, fields)
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


def view(request, pk, media):
    view = get_object_or_404(View.objects.filter(public=True), pk=pk)
    request.user = view.owner  # public views are run as the person who created them
    assert media == "csv"
    query = view.get_query(media)
    return csv_response(request, query)


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
