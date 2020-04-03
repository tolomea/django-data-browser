import csv
import io
from collections import defaultdict

import django.contrib.admin.views.decorators as admin_decorators
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.db import models
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.forms.models import _get_foreign_key
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import TemplateView

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
def query(request, *, app, model, fields="", media):
    query = Query.from_request(app, model, fields, media, request.GET)

    if media == "csv":
        return csv_response(request, query)
    else:
        return html_response(request, query)


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


def html_response(request, query):
    try:
        model = get_model(query)
    except LookupError as e:
        return HttpResponse(e)

    admin_fields = get_all_admin_fields(request)
    fields = get_nested_fields_for_model(model, admin_fields)
    bound_query = BoundQuery(query, fields)
    data = get_data(bound_query)

    return render(
        request, "data_browser/view.html", {"query": bound_query, "data": data}
    )


def view(request, pk, media):
    view = get_object_or_404(View.objects.filter(public=True), pk=pk)
    request.user = view.owner  # public views are run as the person who created them
    assert media == "csv"
    query = view.get_query(media)
    return csv_response(request, query)


catchall = TemplateView.as_view(template_name="data_browser/index.html")
