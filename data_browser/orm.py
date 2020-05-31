from __future__ import annotations

import dataclasses
import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Sequence

from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin, InlineModelAdmin
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.contenttypes.admin import GenericInlineModelAdmin
from django.db import models
from django.db.models import functions
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.forms.models import _get_foreign_key
from django.urls import reverse

from .query import (
    ASC,
    DSC,
    TYPES,
    BooleanFieldType,
    DateFieldType,
    DateTimeFieldType,
    HTMLFieldType,
    MetaFieldType,
    MonthFieldType,
    NumberFieldType,
    StringFieldType,
    WeekDayFieldType,
)

_OPEN_IN_ADMIN = "admin"

_FIELD_MAP = {
    models.BooleanField: BooleanFieldType,
    models.NullBooleanField: BooleanFieldType,
    models.CharField: StringFieldType,
    models.TextField: StringFieldType,
    models.GenericIPAddressField: StringFieldType,
    models.UUIDField: StringFieldType,
    models.DateTimeField: DateTimeFieldType,
    models.DateField: DateFieldType,
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


_AGGREGATES = {
    StringFieldType: ["count"],
    NumberFieldType: ["average", "count", "max", "min", "std_dev", "sum", "variance"],
    DateTimeFieldType: ["count"],  # average, min and max might be nice here but sqlite
    DateFieldType: ["count"],  # average, min and max might be nice here but sqlite
    BooleanFieldType: ["average", "sum"],
}


_FUNC_MAP = {
    "year": (functions.ExtractYear, NumberFieldType),
    "quarter": (functions.ExtractQuarter, NumberFieldType),
    "month": (functions.ExtractMonth, MonthFieldType),
    "day": (functions.ExtractDay, NumberFieldType),
    "week_day": (functions.ExtractWeekDay, WeekDayFieldType),
    "hour": (functions.ExtractHour, NumberFieldType),
    "minute": (functions.ExtractMinute, NumberFieldType),
    "second": (functions.ExtractSecond, NumberFieldType),
    "date": (functions.TruncDate, DateFieldType),
}

if hasattr(functions, "ExtractIsoYear"):  # pragma: no branch
    _FUNC_MAP.update(
        {"iso_year": functions.ExtractIsoYear, "iso_week": functions.ExtractWeek}
    )

_FUNCTIONS = {
    DateTimeFieldType: [
        "year",
        "quarter",
        "month",
        "day",
        "week_day",
        "hour",
        "minute",
        "second",
        "date",
    ],
    DateFieldType: ["year", "quarter", "month", "day", "week_day"],
}


def get_model_name(model, sep="."):
    return f"{model._meta.app_label}{sep}{model.__name__}"


@dataclass
class OrmBoundField:
    orm_field: OrmBaseField = None
    db_field: MetaFieldType = None
    model_path: Sequence[str] = dataclasses.field(default_factory=list)
    pretty_path: Sequence[str] = dataclasses.field(default_factory=list)

    @property
    def field_path(self):
        return self.model_path + [self.db_field.name]

    @property
    def full_path(self):
        # todo this is kinda ugly
        if self.orm_field == self.db_field:
            return self.field_path
        return self.field_path + [self.orm_field.name]

    @property
    def full_path_str(self):
        return "__".join(self.full_path)

    @property
    def field_path_str(self):
        return "__".join(self.field_path)

    @property
    def model_name(self):
        return self.db_field.model_name

    @property
    def concrete(self):
        return self.orm_field.concrete

    @property
    def type_(self):
        return self.orm_field.type_

    @property
    def aggregate(self):
        return self.orm_field.aggregate

    @property
    def function(self):
        return self.orm_field.function


@dataclass
class OrmModel:
    fields: dict
    admin: BaseModelAdmin = None

    @property
    def root(self):
        return bool(self.admin)


class OrmBaseField:
    def __init__(self, model_name, name, pretty_name):
        self.model_name = model_name
        self.name = name
        self.pretty_name = pretty_name

    type_ = None  # can't add
    concrete = False  # can't sort or filter
    rel_name = None  # can't expand

    # internal
    aggregate = None
    function = None

    def __repr__(self):  # pragma: no cover
        params = [
            self.model_name,
            self.name,
            self.pretty_name,
            self.type_,
            self.concrete,
            self.rel_name,
        ]
        return f"{self.__class__.__name__}({', '.join(repr(p) for p in params)})"

    def bind(self, previous):
        previous = previous or OrmBoundField()
        return OrmBoundField(
            self, self, previous.model_path, previous.pretty_path + [self.pretty_name]
        )


class OrmFkField(OrmBaseField):
    def __init__(self, model_name, name, pretty_name, rel_name):
        super().__init__(model_name, name, pretty_name)
        self.rel_name = rel_name

    def bind(self, previous):
        previous = previous or OrmBoundField()
        return OrmBoundField(
            self,
            None,
            previous.model_path + [self.name],
            previous.pretty_path + [self.pretty_name],
        )


class OrmConcreteField(OrmBaseField):
    concrete = True

    def __init__(self, model_name, name, pretty_name, type_):
        super().__init__(model_name, name, pretty_name)
        self.type_ = type_
        self.rel_name = (
            type_.name if type_ in _AGGREGATES or type_ in _FUNCTIONS else None
        )


class OrmCalculatedField(OrmBaseField):
    type_ = StringFieldType


class OrmAdminField(OrmBaseField):
    type_ = HTMLFieldType

    def __init__(self, model_name):
        super().__init__(model_name, _OPEN_IN_ADMIN, _OPEN_IN_ADMIN)


class OrmAggregateField(OrmBaseField):
    type_ = NumberFieldType
    concrete = True

    def __init__(self, model_name, name):
        super().__init__(model_name, name, name)
        self.aggregate = name

    def bind(self, previous):
        assert previous.db_field
        return OrmBoundField(
            self,
            previous.db_field,
            previous.model_path,
            previous.pretty_path + [self.pretty_name],
        )


class OrmFunctionField(OrmBaseField):
    concrete = True

    def __init__(self, model_name, name, type_):
        super().__init__(model_name, name, name)
        self.function = name
        self.type_ = type_

    def bind(self, previous):
        assert previous.db_field
        return OrmBoundField(
            self,
            previous.db_field,
            previous.model_path,
            previous.pretty_path + [self.pretty_name],
        )


def _get_all_admin_fields(request):
    request.data_browser = True

    def from_fieldsets(admin, all_):
        obj = admin.model()  # we want the admin change field sets, not the add ones
        for f in flatten_fieldsets(admin.get_fieldsets(request, obj)):
            # skip calculated fields on inlines
            if not isinstance(admin, InlineModelAdmin) or hasattr(admin.model, f):
                yield f

    def visible(model_admin, request):
        if model_admin.has_change_permission(request):
            return True
        if hasattr(model_admin, "has_view_permission"):
            return model_admin.has_view_permission(request)
        else:
            return False  # pragma: no cover  Django < 2.1 compat

    all_admin_fields = defaultdict(set)
    model_admins = {}
    for model, model_admin in admin.site._registry.items():
        model_admins[model] = model_admin
        if visible(model_admin, request):
            all_admin_fields[model].update(from_fieldsets(model_admin, True))
            all_admin_fields[model].update(model_admin.get_list_display(request))
            all_admin_fields[model].add(_OPEN_IN_ADMIN)

            # check the inlines, these are already filtered for access
            for inline in model_admin.get_inline_instances(request):
                if not isinstance(inline, GenericInlineModelAdmin):  # pragma: no branch
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
        fields.discard("__str__")

    return model_admins, all_admin_fields


def _get_fields_for_model(model, model_admins, admin_fields):
    fields = {}

    model_name = get_model_name(model)
    model_fields = {f.name: f for f in model._meta.get_fields()}

    for field_name in admin_fields[model]:
        field = model_fields.get(field_name)
        if field_name == _OPEN_IN_ADMIN:
            fields[_OPEN_IN_ADMIN] = OrmAdminField(model_name=model_name)
        elif isinstance(field, (ForeignObjectRel, models.ManyToManyField)):
            pass  # TODO 2many support
        elif isinstance(field, models.ForeignKey):
            if field.related_model in admin_fields:
                fields[field_name] = OrmFkField(
                    model_name=model_name,
                    name=field_name,
                    pretty_name=field_name,
                    rel_name=get_model_name(field.related_model),
                )
        elif isinstance(field, type(None)):
            fields[field_name] = OrmCalculatedField(
                model_name=model_name, name=field_name, pretty_name=field_name
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
                fields[field_name] = OrmConcreteField(
                    model_name=model_name,
                    name=field_name,
                    pretty_name=field_name,
                    type_=field_type,
                )
            else:
                logging.getLogger(__name__).warning(
                    f"{model.__name__}.{field_name} unsupported type {type(field).__name__}"
                )

    return OrmModel(fields=fields, admin=model_admins[model])


def _get_fields_for_type(type_):
    aggregates = {
        a: OrmAggregateField(type_.name, a) for a in _AGGREGATES.get(type_, [])
    }
    functions = {
        f: OrmFunctionField(type_.name, f, _FUNC_MAP[f][1])
        for f in _FUNCTIONS.get(type_, [])
    }
    return OrmModel({**aggregates, **functions})


def get_models(request):
    model_admins, admin_fields = _get_all_admin_fields(request)
    models = {
        get_model_name(model): _get_fields_for_model(model, model_admins, admin_fields)
        for model in admin_fields
    }
    types = {type_.name: _get_fields_for_type(type_) for type_ in TYPES.values()}

    return {**models, **types}


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

        filter_str = f"{filter_.orm_bound_field.full_path_str}__{_get_django_lookup(filter_.orm_bound_field.type_, lookup)}"
        if negation:
            return qs.exclude(**{filter_str: filter_.parsed})
        else:
            return qs.filter(**{filter_str: filter_.parsed})

    def fmt(field, value):
        return field.orm_bound_field.type_.format(value)

    request.data_browser = True

    if not bound_query.fields:
        return []

    normal_fields = [f for f in bound_query.fields if not f.orm_bound_field.aggregate]
    calculated_fields = [
        f for f in bound_query.fields if not f.orm_bound_field.concrete
    ]

    admin = bound_query.orm_models[bound_query.model_name].admin
    qs = admin.get_queryset(request)

    # functions
    for field in bound_query.fields + bound_query.filters:
        field = field.orm_bound_field
        if field.function:
            qs = qs.annotate(
                **{
                    field.full_path_str: _FUNC_MAP[field.function][0](
                        field.field_path_str
                    )
                }
            )

    # filter normal and function fields
    for filter_ in bound_query.valid_filters:
        if not filter_.orm_bound_field.aggregate:
            qs = filter(qs)

    # no calculated fields we're going to early out using qs.values
    if not calculated_fields:
        # .values() is interpreted as all values, _ddb_dummy ensures there's always at least one
        qs = qs.values(
            *[f.orm_bound_field.full_path_str for f in normal_fields],
            _ddb_dummy=models.Value(1, output_field=models.IntegerField()),
        )

    # remove duplicates (I think this only happens in the qs.values case)
    qs = qs.distinct()

    # aggregates
    for field in bound_query.fields + bound_query.filters:
        field = field.orm_bound_field
        if field.aggregate:
            qs = qs.annotate(
                **{field.full_path_str: _AGG_MAP[field.aggregate](field.field_path_str)}
            )

    # filter aggregate fields
    for filter_ in bound_query.valid_filters:
        if filter_.orm_bound_field.aggregate:
            qs = filter(qs)

    # sort
    sort_fields = []
    for field in bound_query.sort_fields:
        if field.direction is ASC:
            sort_fields.append(field.orm_bound_field.full_path_str)
        if field.direction is DSC:
            sort_fields.append(f"-{field.orm_bound_field.full_path_str}")
    qs = qs.order_by(*sort_fields)

    # no calculated fields early out using qs.values
    if not calculated_fields:
        results = []
        for row in qs:
            results.append(
                [
                    fmt(field, row[field.orm_bound_field.full_path_str])
                    for field in bound_query.fields
                ]
            )
        return results

    # preloading
    def ancestors(parts):
        for i in range(1, len(parts) + 1):
            yield "__".join(parts[:i])

    select_related = set()
    for field in bound_query.sort_fields:
        select_related.update(ancestors(field.orm_bound_field.model_path))
    for filter_ in bound_query.valid_filters:
        select_related.update(ancestors(filter_.orm_bound_field.model_path))

    prefetch_related = set()
    for field in normal_fields:
        prefetch_related.update(ancestors(field.orm_bound_field.model_path))
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

        if field.aggregate is None and field.function is None:
            *parts, tail = field.full_path
            for part in parts:
                value = getattr(value, part, None)
        else:
            tail = field.full_path_str

        admin = bound_query.orm_models[field.model_name].admin
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
            [
                fmt(field, lookup(row, field.orm_bound_field))
                for field in bound_query.fields
            ]
        )
    return results
