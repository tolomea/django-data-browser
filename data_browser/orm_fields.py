from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from typing import Sequence

from django.contrib.admin.options import BaseModelAdmin
from django.db import models
from django.db.models import functions

from .query import (
    BaseFieldType,
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
        return s(self.full_path)

    @property
    def field_path_str(self):
        return s(self.field_path)

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

    def bind(self, previous):
        previous = previous or OrmBoundField()
        return OrmBoundField(
            self, self, previous.model_path, previous.pretty_path + [self.pretty_name]
        )


class OrmFkField(OrmBaseField):
    def __init__(self, model_name, name, pretty_name, rel_name):
        super().__init__(model_name, name, pretty_name, rel_name=rel_name)

    def bind(self, previous):
        previous = previous or OrmBoundField()
        return OrmBoundField(
            self,
            None,
            previous.model_path + [self.name],
            previous.pretty_path + [self.pretty_name],
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


class OrmCalculatedField(OrmBaseField):
    def __init__(self, model_name, name, pretty_name):
        super().__init__(model_name, name, pretty_name, type_=StringFieldType)


class OrmAdminField(OrmBaseField):
    def __init__(self, model_name):
        super().__init__(
            model_name, _OPEN_IN_ADMIN, _OPEN_IN_ADMIN, type_=HTMLFieldType
        )


class OrmAggregateField(OrmBaseField):
    def __init__(self, model_name, name):
        super().__init__(
            model_name, name, name, type_=NumberFieldType, concrete=True, aggregate=name
        )

    def bind(self, previous):
        assert previous.db_field
        return OrmBoundField(
            self,
            previous.db_field,
            previous.model_path,
            previous.pretty_path + [self.pretty_name],
        )


class OrmFunctionField(OrmBaseField):
    def __init__(self, model_name, name, type_):
        super().__init__(
            model_name, name, name, concrete=True, function=name, type_=type_
        )

    def bind(self, previous):
        assert previous.db_field
        return OrmBoundField(
            self,
            previous.db_field,
            previous.model_path,
            previous.pretty_path + [self.pretty_name],
        )
