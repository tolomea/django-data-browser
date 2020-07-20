from dataclasses import dataclass
from typing import Sequence, Tuple

from django.contrib.admin.options import BaseModelAdmin
from django.db import models
from django.db.models import OuterRef, Subquery, functions
from django.db.models.functions import Cast
from django.urls import reverse

from .query import (
    BaseType,
    BooleanType,
    DateTimeType,
    DateType,
    HTMLType,
    MonthType,
    NumberType,
    StringType,
    WeekDayType,
    YearType,
)

_OPEN_IN_ADMIN = "admin"


_AGG_MAP = {
    "average": lambda x: models.Avg(Cast(x, output_field=models.IntegerField())),
    "count": lambda x: models.Count(x, distinct=True),
    "max": models.Max,
    "min": models.Min,
    "std_dev": models.StdDev,
    "sum": lambda x: models.Sum(Cast(x, output_field=models.IntegerField())),
    "variance": models.Variance,
}


_AGGREGATES = {
    # NTS beware that Sum(type) -> type
    StringType: ["count"],
    NumberType: ["average", "count", "max", "min", "std_dev", "sum", "variance"],
    DateTimeType: ["count"],  # average, min and max might be nice here but sqlite
    DateType: ["count"],  # average, min and max might be nice here but sqlite
    BooleanType: ["average", "sum"],
}


_FUNC_MAP = {
    "year": (functions.ExtractYear, YearType),
    "quarter": (functions.ExtractQuarter, NumberType),
    "month": (functions.ExtractMonth, MonthType),
    "day": (functions.ExtractDay, NumberType),
    "week_day": (functions.ExtractWeekDay, WeekDayType),
    "hour": (functions.ExtractHour, NumberType),
    "minute": (functions.ExtractMinute, NumberType),
    "second": (functions.ExtractSecond, NumberType),
    "date": (functions.TruncDate, DateType),
}

_FUNCTIONS = {
    DateTimeType: [
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
    DateType: ["year", "quarter", "month", "day", "week_day"],
}


def s(path):
    return "__".join(path)


def get_model_name(model, sep="."):
    return f"{model._meta.app_label}{sep}{model.__name__}"


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

    def __post_init__(self):
        if not self.type_:
            assert self.rel_name
        if self.concrete or self.can_pivot:
            assert self.type_

    def format(self, value):
        return self.type_.format(value)


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
    def __init__(self, model_name, name, pretty_name, type_):
        super().__init__(
            model_name,
            name,
            pretty_name,
            concrete=True,
            type_=type_,
            rel_name=(
                type_.name if type_ in _AGGREGATES or type_ in _FUNCTIONS else None
            ),
            can_pivot=True,
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
        from .orm import admin_get_queryset

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
        self, model_name, name, pretty_name, type_, field_type, admin, admin_order_field
    ):
        super().__init__(
            model_name,
            name,
            pretty_name,
            type_=type_,
            can_pivot=True,
            admin=admin,
            concrete=True,
        )
        self.field_type = field_type
        self.admin_order_field = admin_order_field

    def bind(self, previous):
        if previous:
            full_path = previous.full_path + [self.name]
            return OrmBoundAnnotatedField(
                field=self,
                previous=previous,
                full_path=full_path,
                pretty_path=previous.pretty_path + [self.pretty_name],
                queryset_path=f"ddb_{s(full_path)}",
                filter_=True,
            )
        else:
            return OrmBoundField(
                field=self,
                previous=OrmBoundField.blank(),
                full_path=[self.name],
                pretty_path=[self.pretty_name],
                queryset_path=self.name,
                filter_=True,
            )


class OrmAdminField(OrmBaseField):
    def __init__(self, model_name):
        super().__init__(
            model_name, _OPEN_IN_ADMIN, _OPEN_IN_ADMIN, type_=HTMLType, can_pivot=True
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


class OrmAggregateField(OrmBaseField):
    def __init__(self, model_name, name):
        super().__init__(model_name, name, name, type_=NumberType, concrete=True)
        self.aggregate = name

    def bind(self, previous):
        assert previous
        full_path = previous.full_path + [self.name]
        agg = _AGG_MAP[self.aggregate](s(previous.full_path))
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=s(full_path),
            aggregate_clause=(s(full_path), agg),
            having=True,
        )


class OrmBoundFunctionField(OrmBoundField):
    def annotate(self, request, qs):
        return qs.annotate(
            **{
                self.queryset_path: _FUNC_MAP[self.function][0](
                    s(self.previous.full_path)
                )
            }
        )


class OrmFunctionField(OrmBaseField):
    def __init__(self, model_name, name, type_):
        super().__init__(
            model_name, name, name, type_=type_, concrete=True, can_pivot=True
        )
        self.function = name

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
