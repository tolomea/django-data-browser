from collections import defaultdict
from dataclasses import dataclass

from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.admin.utils import flatten_fieldsets
from django.db import models
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.forms.models import _get_foreign_key
from django.urls import reverse

from .query import (
    ASC,
    DSC,
    BooleanFieldType,
    FieldType,
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


def get_model_name(model, sep="."):
    return f"{model._meta.app_label}{sep}{model.__name__}"


@dataclass
class OrmModel:
    fields: dict
    fks: dict
    admin: BaseModelAdmin = None


@dataclass
class OrmField:
    type_: FieldType
    concrete: bool


@dataclass
class OrmFkField:
    model_name: str


def _get_all_admin_fields(request):
    request.data_browser = True

    def from_fieldsets(admin, model):
        obj = model()  # we want the admin change field sets, not the add ones
        for f in flatten_fieldsets(admin.get_fieldsets(request, obj)):
            if hasattr(model, f):
                yield f

    def visible(modeladmin, request):
        if modeladmin.has_change_permission(request):
            return True
        if hasattr(modeladmin, "has_view_permission"):
            return modeladmin.has_view_permission(request)
        return False

    all_admin_fields = defaultdict(set)
    model_admins = {}
    for model, modeladmin in admin.site._registry.items():
        model_admins[model] = modeladmin
        if visible(modeladmin, request):
            all_admin_fields[model].update(from_fieldsets(modeladmin, model))
            all_admin_fields[model].add(_OPEN_IN_ADMIN)

            # check the inlines, these are already filtered for access
            for inline in modeladmin.get_inline_instances(request):
                if inline.model not in model_admins:  # pragma: no cover
                    model_admins[inline.model] = inline
                all_admin_fields[inline.model].update(
                    from_fieldsets(inline, inline.model)
                )
                all_admin_fields[inline.model].add(
                    _get_foreign_key(model, inline.model, inline.fk_name).name
                )

    # we always have id and never pk
    for fields in all_admin_fields.values():
        fields.add("id")
        fields.discard("pk")

    return model_admins, all_admin_fields


def _get_fields_for_model(model, model_admins, admin_fields):
    fields = {}
    fks = {}

    model_fields = {f.name: f for f in model._meta.get_fields()}

    for field_name in admin_fields[model]:
        field = model_fields.get(field_name)
        if field_name == _OPEN_IN_ADMIN:
            fields[_OPEN_IN_ADMIN] = OrmField(type_=HTMLFieldType, concrete=False)
        elif isinstance(field, (ForeignObjectRel, models.ManyToManyField)):
            pass  # TODO 2many support
        elif isinstance(field, models.ForeignKey):
            if field.related_model in admin_fields:
                fks[field_name] = OrmFkField(get_model_name(field.related_model))
        elif isinstance(field, type(None)):
            fields[field_name] = OrmField(type_=StringFieldType, concrete=False)
        else:
            for django_types, field_type in _FIELD_MAP:
                if isinstance(field, django_types):
                    if field_type:
                        fields[field_name] = OrmField(type_=field_type, concrete=True)
                    break
            else:  # pragma: no cover
                print(
                    f"DataBrowser: {model.__name__}.{field_name} unknown type {type(field).__name__}"
                )

    return OrmModel(fields=fields, fks=fks, admin=model_admins[model])


def get_models(request):
    model_admins, admin_fields = _get_all_admin_fields(request)
    # {model: {"fields": {field_name, FieldType}, "fks": {field_name: model}}}
    return {
        get_model_name(model): _get_fields_for_model(model, model_admins, admin_fields)
        for model in admin_fields
    }


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


def get_data(request, bound_query):
    request.data_browser = True

    if not bound_query.fields:
        return []

    admin = bound_query.orm_models[bound_query.model_name].admin
    qs = admin.get_queryset(request)

    # sort
    sort_fields = []
    for field in bound_query.sort_fields:
        if field.direction is ASC:
            sort_fields.append(field.path)
        if field.direction is DSC:
            sort_fields.append(f"-{field.path}")
    qs = qs.order_by(*sort_fields)

    # filter
    for filter_ in bound_query.filters:
        if filter_.is_valid:
            negation = False

            lookup = filter_.lookup
            if lookup.startswith("not_"):
                negation = True
                lookup = lookup[4:]

            filter_str = f"{filter_.path}__{_get_django_lookup(filter_.type_, lookup)}"
            if negation:
                qs = qs.exclude(**{filter_str: filter_.parsed})
            else:
                qs = qs.filter(**{filter_str: filter_.parsed})

    # no calculated fields early out using qs.values
    if not bound_query.calculated_fields:
        data = []
        for row in qs.values(*[f.path for f in bound_query.fields]).distinct():
            data.append(
                [field.type_.format(row[field.path]) for field in bound_query.fields]
            )
        return data

    # preloading
    select_related = set()

    def add_select_relateds(path):
        while "__" in path:
            path = path.rsplit("__", 1)[0]
            select_related.add(path)

    for field in bound_query.sort_fields:
        add_select_relateds(field.path)

    for filter_ in bound_query.filters:
        if filter_.is_valid:
            add_select_relateds(filter_.path)

    prefetch_related = set()
    for field in bound_query.fields:
        if "__" in field.path:
            prefetch_related.add(field.path.rsplit("__", 1)[0])
    prefetch_related -= select_related

    if select_related:
        qs = qs.select_related(*select_related)
    if prefetch_related:
        qs = qs.prefetch_related(*prefetch_related)

    def get_admin_link(obj):
        if obj is None:
            return "null"
        model_name = get_model_name(obj.__class__, "_")
        url_name = f"admin:{model_name}_change".lower()
        url = reverse(url_name, args=[obj.pk])
        return f'<a href="{url}">{obj}</a>'

    # get data
    def lookup(obj, path):
        value = obj
        for part in path.split("__"):
            if part == _OPEN_IN_ADMIN:
                value = get_admin_link(value)
            else:
                value = getattr(value, part, None)
        return value() if callable(value) else value

    data = []
    for row in qs.distinct():
        data.append(
            [
                field.type_.format(lookup(row, field.path))
                for field in bound_query.fields
            ]
        )
    return data
