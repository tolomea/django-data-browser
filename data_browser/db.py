from collections import defaultdict

from django.apps import apps
from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.db import models
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.forms.models import _get_foreign_key
from django.urls import reverse

from .query import (
    ASC,
    DSC,
    BooleanFieldType,
    HTMLFieldType,
    NumberFieldType,
    StringFieldType,
    TimeFieldType,
)

_OPEN_IN_ADMIN = "admin"

_FIELD_MAP = [
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
    ((models.FileField,), None),
]


def get_model(app, model):
    return apps.get_model(app_label=app, model_name=model)


def model_name(model, sep="."):
    return f"{model._meta.app_label}{sep}{model.__name__}"


def _get_all_admin_fields(request):
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


def _get_fields_for_model(model, admin_fields):
    # {"fields": {field_name, FieldType}, "fks": {field_name: model}}
    fields = {_OPEN_IN_ADMIN: {"type": HTMLFieldType, "concrete": False}}
    fks = {}

    model_fields = {f.name: f for f in model._meta.get_fields()}
    if "id" in model_fields:
        model_fields["pk"] = model_fields["id"]

    for field_name in admin_fields[model]:
        field = model_fields.get(field_name)
        if isinstance(field, (ForeignObjectRel, models.ManyToManyField)):
            pass  # TODO 2many support
        elif isinstance(field, models.ForeignKey):
            fks[field_name] = field.related_model
        elif isinstance(field, type(None)):
            fields[field_name] = {"type": StringFieldType, "concrete": False}
        else:
            for django_types, field_type in _FIELD_MAP:
                if isinstance(field, django_types):
                    if field_type:
                        fields[field_name] = {"type": field_type, "concrete": True}
                    break
            else:  # pragma: no cover
                print(
                    f"DataBrowser: {model.__name__}.{field_name} unknown type {type(field).__name__}"
                )

    return {"fields": fields, "fks": fks}


def get_all_model_fields(request):
    admin_fields = _get_all_admin_fields(request)
    # {model: {"fields": {field_name, FieldType}, "fks": {field_name: model}}}
    return {model: _get_fields_for_model(model, admin_fields) for model in admin_fields}


def _get_django_lookup(field_type, lookup):
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

            filter_str = f"{filter_.name}__{_get_django_lookup(filter_.field, lookup)}"
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

    def get_admin_link(obj):
        model = model_name(obj.__class__, "_")
        url_name = f"admin:{model}_change".lower()
        url = reverse(url_name, args=[obj.pk])
        return f'<a href="{url}">{obj}</a>'

    # get data
    def lookup(obj, name):
        value = obj
        for part in name.split("__"):
            if part == _OPEN_IN_ADMIN:
                value = get_admin_link(value)
            else:
                value = getattr(value, part, None)
        return value() if callable(value) else value

    data = []
    for row in qs.distinct():
        data.append([t.format(lookup(row, f)) for f, t in bound_query.fields.items()])
    return data
