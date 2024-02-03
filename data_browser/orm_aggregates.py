from dataclasses import dataclass

from django.conf import settings
from django.db import models
from django.db.models import DurationField
from django.db.models import IntegerField
from django.db.models import Value
from django.db.models.functions import Cast

from data_browser.orm_fields import OrmBaseField
from data_browser.orm_fields import OrmBoundField
from data_browser.types import ARRAY_TYPES
from data_browser.types import TYPES
from data_browser.types import BaseType
from data_browser.types import BooleanType
from data_browser.types import DateTimeType
from data_browser.types import DateType
from data_browser.types import DurationType
from data_browser.types import NumberType
from data_browser.util import annotation_path

try:
    from django.contrib.postgres.aggregates import ArrayAgg
except ModuleNotFoundError:  # pragma: no cover
    ArrayAgg = None


class OrmAggregateField(OrmBaseField):
    def __init__(self, base_type, name, agg):
        super().__init__(
            base_type.name, name, name.replace("_", " "), type_=agg.type_, concrete=True
        )
        self.base_type = base_type
        self.func = agg.func

    def bind(self, previous):
        assert previous
        assert previous.type_ == self.base_type
        full_path = previous.full_path + [self.name]
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=full_path,
            verbose_path=previous.verbose_path + [self.verbose_name],
            queryset_path=[annotation_path(full_path)],
            aggregate_clause=self.func(previous.queryset_path_str),
            having=True,
        )


class _CastDuration(Cast):
    def __init__(self, expression):
        super().__init__(expression, output_field=DurationField())

    def as_mysql(self, compiler, connection, **extra_context):
        # https://github.com/django/django/pull/13398
        template = "%(function)s(%(expressions)s AS signed integer)"
        return self.as_sql(compiler, connection, template=template, **extra_context)


@dataclass
class Agg:
    func: callable
    type_: BaseType


TYPE_AGGREGATES = {type_: {} for type_ in TYPES.values()}

for type_ in TYPES.values():
    if type_ != BooleanType:
        TYPE_AGGREGATES[type_]["count"] = Agg(
            lambda x: models.Count(x, distinct=True), NumberType
        )

for type_ in [DateTimeType, DateType, DurationType, NumberType]:
    TYPE_AGGREGATES[type_]["max"] = Agg(models.Max, type_)
    TYPE_AGGREGATES[type_]["min"] = Agg(models.Min, type_)

TYPE_AGGREGATES[NumberType]["average"] = Agg(models.Avg, NumberType)
TYPE_AGGREGATES[NumberType]["std_dev"] = Agg(models.StdDev, NumberType)
TYPE_AGGREGATES[NumberType]["sum"] = Agg(models.Sum, NumberType)
TYPE_AGGREGATES[NumberType]["variance"] = Agg(models.Variance, NumberType)

TYPE_AGGREGATES[DurationType]["average"] = Agg(
    lambda x: models.Avg(_CastDuration(x)), DurationType
)
TYPE_AGGREGATES[DurationType]["sum"] = Agg(
    lambda x: models.Sum(_CastDuration(x)), DurationType
)

TYPE_AGGREGATES[BooleanType]["average"] = Agg(
    lambda x: models.Avg(Cast(x, output_field=IntegerField())), NumberType
)
TYPE_AGGREGATES[BooleanType]["sum"] = Agg(
    lambda x: models.Sum(Cast(x, output_field=IntegerField())), NumberType
)

if "postgresql" in settings.DATABASES["default"]["ENGINE"]:
    for array_type in ARRAY_TYPES.values():
        if array_type.raw_type is None:
            TYPE_AGGREGATES[array_type.element_type]["all"] = Agg(
                lambda x: ArrayAgg(x, default=Value([]), distinct=True, ordering=x),
                array_type,
            )


def get_aggregates_for_type(type_):
    return {
        name: OrmAggregateField(type_, name, agg)
        for name, agg in TYPE_AGGREGATES[type_].items()
    }
