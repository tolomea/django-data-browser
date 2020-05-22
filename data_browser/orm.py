from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass

from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin, InlineModelAdmin
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

_FIELD_MAP = {
    models.BooleanField: BooleanFieldType,
    models.NullBooleanField: BooleanFieldType,
    models.CharField: StringFieldType,
    models.TextField: StringFieldType,
    models.GenericIPAddressField: StringFieldType,
    models.UUIDField: StringFieldType,
    models.DateTimeField: TimeFieldType,
    models.DateField: TimeFieldType,
    models.DecimalField: NumberFieldType,
    models.FloatField: NumberFieldType,
    models.IntegerField: NumberFieldType,
    models.AutoField: NumberFieldType,
}

_AGG_MAP = {
    "average": models.Avg,
    "count": lambda x: models.Count(x, distinct=True),
    "max": models.Max,
    "min": models.Min,
    "std_dev": models.StdDev,
    "sum": models.Sum,
    "variance": models.Variance,
}


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
    model_name: str


@dataclass
class OrmFkField:
    model_name: str


def _get_all_admin_fields(request):
    request.data_browser = True

    def from_fieldsets(admin, all_):
        obj = admin.model()  # we want the admin change field sets, not the add ones
        for f in flatten_fieldsets(admin.get_fieldsets(request, obj)):
            # skip calculated fields on inlines
            if not isinstance(admin, InlineModelAdmin) or hasattr(admin.model, f):
                yield f

    def visible(modeladmin, request):
        if modeladmin.has_change_permission(request):
            return True
        if hasattr(modeladmin, "has_view_permission"):
            return modeladmin.has_view_permission(request)
        else:
            return False  # pragma: no cover  Django < 2.1 compat

    all_admin_fields = defaultdict(set)
    model_admins = {}
    for model, modeladmin in admin.site._registry.items():
        model_admins[model] = modeladmin
        if visible(modeladmin, request):
            all_admin_fields[model].update(from_fieldsets(modeladmin, True))
            all_admin_fields[model].add(_OPEN_IN_ADMIN)

            # check the inlines, these are already filtered for access
            for inline in modeladmin.get_inline_instances(request):
                if inline.model not in model_admins:  # pragma: no branch
                    model_admins[inline.model] = inline
                all_admin_fields[inline.model].update(from_fieldsets(inline, False))
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

    model_name = get_model_name(model)
    model_fields = {f.name: f for f in model._meta.get_fields()}

    for field_name in admin_fields[model]:
        field = model_fields.get(field_name)
        if field_name == _OPEN_IN_ADMIN:
            fields[_OPEN_IN_ADMIN] = OrmField(
                type_=HTMLFieldType, concrete=False, model_name=model_name
            )
        elif isinstance(field, (ForeignObjectRel, models.ManyToManyField)):
            pass  # TODO 2many support
        elif isinstance(field, models.ForeignKey):
            if field.related_model in admin_fields:
                fks[field_name] = OrmFkField(get_model_name(field.related_model))
        elif isinstance(field, type(None)):
            fields[field_name] = OrmField(
                type_=StringFieldType, concrete=False, model_name=model_name
            )
        else:
            if field.__class__ in _FIELD_MAP:
                field_type = _FIELD_MAP[field.__class__]
            else:
                for django_type, field_type in _FIELD_MAP.items():
                    if isinstance(field, django_type):
                        break
                else:
                    field_type = None

            if field_type:
                fields[field_name] = OrmField(
                    type_=field_type, concrete=True, model_name=model_name
                )
            else:
                logging.getLogger(__name__).warning(
                    f"{model.__name__}.{field_name} unsupported type {type(field).__name__}"
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


def get_results(request, bound_query):
    def filter(qs):
        negation = False

        lookup = filter_.lookup
        if lookup.startswith("not_"):
            negation = True
            lookup = lookup[4:]

        filter_str = f"{filter_.path}__{_get_django_lookup(filter_.type_, lookup)}"
        if negation:
            return qs.exclude(**{filter_str: filter_.parsed})
        else:
            return qs.filter(**{filter_str: filter_.parsed})

    request.data_browser = True

    if not bound_query.fields:
        return []

    normal_fields = [f for f in bound_query.fields if not f.aggregate]

    admin = bound_query.orm_models[bound_query.model_name].admin
    qs = admin.get_queryset(request)

    # filter normal fields
    for filter_ in bound_query.valid_filters:
        if not filter_.aggregate:
            qs = filter(qs)

    # no calculated fields we're going to early out using qs.values
    if not bound_query.calculated_fields:
        # .values() is interpreted as all values, _ddb_dummy ensures there's always at least one
        qs = qs.values(
            *[f.path for f in normal_fields],
            _ddb_dummy=models.Value(1, output_field=models.IntegerField()),
        )

    # remove duplicates (I think this only happens in the qs.values case)
    qs = qs.distinct()

    # aggregates
    for field in bound_query.fields + bound_query.filters:
        if field.aggregate:
            qs = qs.annotate(
                **{field.path: _AGG_MAP[field.aggregate](field.field_path)}
            )

    # filter aggregate fields
    for filter_ in bound_query.valid_filters:
        if filter_.aggregate:
            qs = filter(qs)

    # sort
    sort_fields = []
    for field in bound_query.sort_fields:
        if field.direction is ASC:
            sort_fields.append(field.path)
        if field.direction is DSC:
            sort_fields.append(f"-{field.path}")
    qs = qs.order_by(*sort_fields)

    # no calculated fields early out using qs.values
    if not bound_query.calculated_fields:
        results = []
        for row in qs:
            results.append(
                [field.type_.format(row[field.path]) for field in bound_query.fields]
            )
        return results

    # preloading
    def ancestors(parts):
        for i in range(1, len(parts) + 1):
            yield "__".join(parts[:i])

    select_related = set()
    for field in bound_query.sort_fields:
        select_related.update(ancestors(field.path_parts))
    for filter_ in bound_query.valid_filters:
        select_related.update(ancestors(filter_.path_parts))

    prefetch_related = set()
    for field in normal_fields:
        prefetch_related.update(ancestors(field.path_parts))
    prefetch_related -= select_related

    if select_related:
        qs = qs.select_related(*select_related)
    if prefetch_related:
        qs = qs.prefetch_related(*prefetch_related)

    # get results
    def get_admin_link(obj):
        if obj is None:
            return None
        model_name = get_model_name(obj.__class__, "_")
        url_name = f"admin:{model_name}_change".lower()
        url = reverse(url_name, args=[obj.pk])
        return f'<a href="{url}">{obj}</a>'

    def lookup(obj, field):
        value = obj

        if field.aggregate is None:
            *parts, tail = field.path.split("__")
            for part in parts:
                value = getattr(value, part, None)
        else:
            tail = field.path

        admin = bound_query.orm_models[field.orm_field.model_name].admin
        if field.concrete:
            return getattr(value, tail, None)
        elif tail == _OPEN_IN_ADMIN:
            return get_admin_link(value)
        elif hasattr(admin, tail):
            try:
                func = getattr(admin, tail)
                return value and func(value)
            except Exception as e:
                return str(e)
        else:
            try:
                value = getattr(value, tail, None)
                return value() if callable(value) else value
            except Exception as e:
                return str(e)

    results = []
    for row in qs:
        results.append(
            [field.type_.format(lookup(row, field)) for field in bound_query.fields]
        )
    return results
