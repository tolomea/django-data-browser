from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Tuple

from django.contrib.admin.options import BaseModelAdmin
from django.db import models
from django.db.models import functions

from .query import (
    BaseFieldType,
    BooleanFieldType,
    DateFieldType,
    DateTimeFieldType,
    HTMLFieldType,
    MonthFieldType,
    NumberFieldType,
    StringFieldType,
    WeekDayFieldType,
)

_OPEN_IN_ADMIN = "admin"


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


def s(path):
    return "__".join(path)


@dataclass
class OrmBoundField:
    full_path: Sequence[str]
    pretty_path: Sequence[str]
    type_: BaseFieldType = None
    queryset_path: str = None
    function_clause: Tuple[str, models.Func] = None
    aggregate_clause: Tuple[str, models.Func] = None
    filter_: bool = False
    group_by: bool = False
    having: bool = False
    model_name: str = None
    admin_link: bool = False


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
    type_: BaseFieldType = None
    concrete: bool = False
    rel_name: str = None
    # internal
    aggregate: str = None
    function: str = None

    def __post_init__(self):
        if not self.type_:
            assert self.rel_name
        if self.concrete:
            assert self.type_
        if self.aggregate or self.function:
            assert self.concrete
            assert not self.rel_name


class OrmFkField(OrmBaseField):
    def __init__(self, model_name, name, pretty_name, rel_name):
        super().__init__(model_name, name, pretty_name, rel_name=rel_name)

    def bind(self, previous):
        previous = previous or OrmBoundField(full_path=[], pretty_path=[])
        full_path = previous.full_path + [self.name]
        return OrmBoundField(
            full_path=full_path, pretty_path=previous.pretty_path + [self.pretty_name]
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
        )

    def bind(self, previous):
        previous = previous or OrmBoundField(full_path=[], pretty_path=[])
        full_path = previous.full_path + [self.name]
        return OrmBoundField(
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            type_=self.type_,
            queryset_path=s(full_path),
            filter_=True,
            group_by=True,
        )


class OrmCalculatedField(OrmBaseField):
    def __init__(self, model_name, name, pretty_name):
        super().__init__(model_name, name, pretty_name, type_=StringFieldType)

    def bind(self, previous):
        previous = previous or OrmBoundField(full_path=[], pretty_path=[])
        full_path = previous.full_path + [self.name]
        return OrmBoundField(
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            type_=self.type_,
            queryset_path=s(previous.full_path + ["id"]),
            group_by=True,
            model_name=self.model_name,
        )


class OrmAdminField(OrmBaseField):
    def __init__(self, model_name):
        super().__init__(
            model_name, _OPEN_IN_ADMIN, _OPEN_IN_ADMIN, type_=HTMLFieldType
        )

    def bind(self, previous):
        previous = previous or OrmBoundField(full_path=[], pretty_path=[])
        full_path = previous.full_path + [self.name]
        return OrmBoundField(
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            type_=self.type_,
            queryset_path=s(previous.full_path + ["id"]),
            group_by=True,
            model_name=self.model_name,
            admin_link=True,
        )


class OrmAggregateField(OrmBaseField):
    def __init__(self, model_name, name):
        super().__init__(
            model_name, name, name, type_=NumberFieldType, concrete=True, aggregate=name
        )

    def bind(self, previous):
        assert previous
        full_path = previous.full_path + [self.name]
        agg = _AGG_MAP[self.aggregate](s(previous.full_path))
        return OrmBoundField(
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            type_=self.type_,
            queryset_path=s(full_path),
            aggregate_clause=(s(full_path), agg),
            having=True,
        )


class OrmFunctionField(OrmBaseField):
    def __init__(self, model_name, name, type_):
        super().__init__(
            model_name, name, name, concrete=True, function=name, type_=type_
        )

    def bind(self, previous):
        assert previous
        full_path = previous.full_path + [self.name]
        func = _FUNC_MAP[self.function][0](s(previous.full_path))
        return OrmBoundField(
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            type_=self.type_,
            queryset_path=s(full_path),
            function_clause=(s(full_path), func),
            filter_=True,
            group_by=True,
        )
