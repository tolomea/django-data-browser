from collections import defaultdict
from dataclasses import dataclass
from typing import Sequence, Tuple

import django
from django.contrib.admin.options import BaseModelAdmin
from django.db import models
from django.db.models import (
    BooleanField,
    DateField,
    ExpressionWrapper,
    IntegerField,
    OuterRef,
    Q,
    Subquery,
    functions,
)
from django.db.models.functions import Cast
from django.urls import reverse
from django.utils.html import format_html

from .types import (
    BaseType,
    BooleanType,
    DateTimeType,
    DateType,
    HTMLType,
    IsNullType,
    MonthType,
    NumberType,
    StringChoiceType,
    StringType,
    WeekDayType,
    YearType,
)

OPEN_IN_ADMIN = "admin"

_TYPE_AGGREGATES = defaultdict(
    lambda: ["count"],
    {
        StringType: ["count"],
        StringChoiceType: ["count"],
        NumberType: ["average", "count", "max", "min", "std_dev", "sum", "variance"],
        DateTimeType: ["count"],  # average, min and max might be nice here but sqlite
        DateType: ["count"],  # average, min and max might be nice here but sqlite
        BooleanType: ["average", "sum"],
        YearType: ["count", "average"],
    },
)


_DATE_FUNCTIONS = [
    "is_null",
    "year",
    "quarter",
    "month",
    "day",
    "week_day",
    "month_start",
]
if django.VERSION >= (2, 2):  # pragma: no branch
    _DATE_FUNCTIONS += ["iso_year", "iso_week", "week_start"]
_TYPE_FUNCTIONS = defaultdict(
    lambda: ["is_null"],
    {
        DateType: _DATE_FUNCTIONS,
        DateTimeType: _DATE_FUNCTIONS + ["hour", "minute", "second", "date"],
    },
)


def _get_django_aggregate(field_type, name):
    if field_type == BooleanType:
        return {
            "average": lambda x: models.Avg(Cast(x, output_field=IntegerField())),
            "sum": lambda x: models.Sum(Cast(x, output_field=IntegerField())),
        }[name]
    else:
        return {
            # these all have result type number
            "average": models.Avg,
            "count": lambda x: models.Count(x, distinct=True),
            "max": models.Max,
            "min": models.Min,
            "std_dev": models.StdDev,
            "sum": models.Sum,
            "variance": models.Variance,
        }[name]


def _get_django_lookup(field_type, lookup, filter_value):
    from .types import StringChoiceType, StringType

    if lookup == "field_equals":
        lookup, filter_value = filter_value
        return lookup, filter_value
    elif field_type in [StringType, StringChoiceType]:
        return (
            {
                "equals": "iexact",
                "regex": "iregex",
                "contains": "icontains",
                "starts_with": "istartswith",
                "ends_with": "iendswith",
                "is_null": "isnull",
            }[lookup],
            filter_value,
        )
    else:
        return (
            {
                "equals": "exact",
                "is_null": "isnull",
                "gt": "gt",
                "gte": "gte",
                "lt": "lt",
                "lte": "lte",
                "contains": "contains",
                "length": "len",
                "has_key": "has_key",
            }[lookup],
            filter_value,
        )


def IsNull(field_name):
    return ExpressionWrapper(Q(**{field_name: None}), output_field=BooleanField())


def _get_django_function(name):
    mapping = {
        "year": (functions.ExtractYear, YearType),
        "quarter": (functions.ExtractQuarter, NumberType),
        "month": (functions.ExtractMonth, MonthType),
        "month_start": (lambda x: functions.TruncMonth(x, DateField()), DateType),
        "day": (functions.ExtractDay, NumberType),
        "week_day": (functions.ExtractWeekDay, WeekDayType),
        "hour": (functions.ExtractHour, NumberType),
        "minute": (functions.ExtractMinute, NumberType),
        "second": (functions.ExtractSecond, NumberType),
        "date": (functions.TruncDate, DateType),
        "is_null": (IsNull, IsNullType),
    }
    if django.VERSION >= (2, 2):  # pragma: no branch
        mapping.update(
            {
                "iso_year": (functions.ExtractIsoYear, YearType),
                "iso_week": (functions.ExtractWeek, NumberType),
                "week_start": (lambda x: functions.TruncWeek(x, DateField()), DateType),
            }
        )
    return mapping[name]


def s(path):
    return "__".join(path)


def get_model_name(model, sep="."):
    return f"{model._meta.app_label}{sep}{model.__name__}"


def get_fields_for_type(type_):
    aggregates = {a: OrmAggregateField(type_.name, a) for a in _TYPE_AGGREGATES[type_]}
    functions = {
        f: OrmFunctionField(type_.name, f, _get_django_function(f)[1])
        for f in _TYPE_FUNCTIONS[type_]
    }
    return {**aggregates, **functions}


@dataclass
class OrmBoundField:
    field: "OrmBaseField"
    previous: "OrmBoundField"
    full_path: Sequence[str]
    pretty_path: Sequence[str]
    queryset_path: str = None
    aggregate_clause: Tuple[str, models.Func] = None
    filter_: bool = False
    having: bool = False
    model_name: str = None

    @property
    def path_str(self):
        return s(self.full_path)

    @property
    def group_by(self):
        return self.field.can_pivot

    def annotate(self, request, qs):
        return qs

    def __getattr__(self, name):
        return getattr(self.field, name)

    @classmethod
    def blank(cls):
        return cls(field=None, previous=None, full_path=[], pretty_path=[])

    def get_format_hints(self, data):
        return self.type_.get_format_hints(self.path_str, data)


@dataclass
class OrmModel:
    fields: dict
    admin: BaseModelAdmin = None

    @property
    def root(self):
        return bool(self.admin)


@dataclass
class OrmBaseField:
    model_name: str
    name: str
    pretty_name: str
    type_: BaseType = None
    concrete: bool = False
    rel_name: str = None
    can_pivot: bool = False
    admin: object = None
    choices: Sequence[Tuple[str, str]] = ()

    def __post_init__(self):
        if not self.type_:
            assert self.rel_name
        if self.concrete or self.can_pivot:
            assert self.type_

    def format(self, value):
        return self.type_.format(value, self.choices)


class OrmFkField(OrmBaseField):
    def __init__(self, model_name, name, pretty_name, rel_name):
        super().__init__(model_name, name, pretty_name, rel_name=rel_name)

    def bind(self, previous):
        previous = previous or OrmBoundField.blank()
        full_path = previous.full_path + [self.name]
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
        )


class OrmConcreteField(OrmBaseField):
    def __init__(self, model_name, name, pretty_name, type_, rel_name, choices=None):
        super().__init__(
            model_name,
            name,
            pretty_name,
            concrete=True,
            type_=type_,
            rel_name=rel_name,
            can_pivot=True,
            choices=choices or (),
        )

    def bind(self, previous):
        previous = previous or OrmBoundField.blank()
        full_path = previous.full_path + [self.name]
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=s(full_path),
            filter_=True,
        )


class OrmCalculatedField(OrmBaseField):
    def __init__(self, model_name, name, pretty_name, admin):
        super().__init__(
            model_name, name, pretty_name, type_=StringType, can_pivot=True, admin=admin
        )

    def bind(self, previous):
        previous = previous or OrmBoundField.blank()
        full_path = previous.full_path + [self.name]
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=s(previous.full_path + ["id"]),
            model_name=self.model_name,
        )

    def format(self, obj):
        if obj is None:
            return None

        if hasattr(self.admin, self.name):
            # admin callable
            func = getattr(self.admin, self.name)
            try:
                return func(obj)
            except Exception as e:
                return str(e)
        else:
            # model property or callable
            try:
                value = getattr(obj, self.name)
                return value() if callable(value) else value
            except Exception as e:
                return str(e)


class OrmBoundAnnotatedField(OrmBoundField):
    def annotate(self, request, qs):
        from .orm_results import admin_get_queryset

        return qs.annotate(
            **{
                self.queryset_path: Subquery(
                    admin_get_queryset(self.admin, request, [self.name])
                    .filter(pk=OuterRef(s(self.previous.full_path + ["id"])))
                    .values(self.admin_order_field)[:1],
                    output_field=self.field_type,
                )
            }
        )


class OrmAnnotatedField(OrmBaseField):
    def __init__(
        self,
        model_name,
        name,
        pretty_name,
        type_,
        field_type,
        admin,
        admin_order_field,
        choices=None,
    ):
        super().__init__(
            model_name,
            name,
            pretty_name,
            type_=type_,
            can_pivot=True,
            admin=admin,
            concrete=True,
            choices=choices or (),
        )
        self.field_type = field_type
        self.admin_order_field = admin_order_field

    def bind(self, previous):
        previous = previous or OrmBoundField.blank()

        full_path = previous.full_path + [self.name]
        return OrmBoundAnnotatedField(
            field=self,
            previous=previous,
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=f"ddb_{s(full_path)}",
            filter_=True,
        )


class OrmAdminField(OrmBaseField):
    def __init__(self, model_name):
        super().__init__(
            model_name, OPEN_IN_ADMIN, OPEN_IN_ADMIN, type_=HTMLType, can_pivot=True
        )

    def bind(self, previous):
        previous = previous or OrmBoundField.blank()
        full_path = previous.full_path + [self.name]
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=s(previous.full_path + ["id"]),
            model_name=self.model_name,
        )

    def format(self, obj):
        if obj is None:
            return None

        model_name = get_model_name(obj.__class__, "_")
        url_name = f"admin:{model_name}_change".lower()
        url = reverse(url_name, args=[obj.pk])
        return f'<a href="{url}">{obj}</a>'


class OrmFileField(OrmConcreteField):
    def __init__(self, model_name, name, pretty_name, django_field):
        super().__init__(
            model_name, name, pretty_name, type_=HTMLType, rel_name=HTMLType.name
        )
        self.django_field = django_field

    def format(self, value):
        if not value:
            return None
        try:
            # some storage backends will hard fail if their underlying storage isn't
            # setup right https://github.com/tolomea/django-data-browser/issues/11
            return format_html(
                '<a href="{}">{}</a>', self.django_field.storage.url(value), value
            )
        except Exception as e:
            return str(e)


class OrmAggregateField(OrmBaseField):
    def __init__(self, model_name, name):
        super().__init__(model_name, name, name, type_=NumberType, concrete=True)

    def bind(self, previous):
        assert previous
        full_path = previous.full_path + [self.name]
        agg_func = _get_django_aggregate(previous.type_, self.name)
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=s(full_path),
            aggregate_clause=(s(full_path), agg_func(s(previous.full_path))),
            having=True,
        )


class OrmBoundFunctionField(OrmBoundField):
    def annotate(self, request, qs):
        func = _get_django_function(self.name)[0](s(self.previous.full_path))
        return qs.annotate(**{self.queryset_path: func})


class OrmFunctionField(OrmBaseField):
    def __init__(self, model_name, name, type_):
        super().__init__(
            model_name, name, name, type_=type_, concrete=True, can_pivot=True
        )

    def bind(self, previous):
        assert previous
        full_path = previous.full_path + [self.name]
        return OrmBoundFunctionField(
            field=self,
            previous=previous,
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=s(full_path),
            filter_=True,
        )
