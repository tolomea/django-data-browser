from django.conf import settings
from django.db import models
from django.db.models import DurationField, IntegerField, Value
from django.db.models.functions import Cast

from .orm_fields import OrmBaseField, OrmBoundField
from .types import (
    TYPES,
    ArrayTypeMixin,
    BooleanType,
    DateTimeType,
    DateType,
    DurationType,
    NumberType,
)
from .util import annotation_path

try:
    from django.contrib.postgres.aggregates import ArrayAgg
except ModuleNotFoundError:  # pragma: no cover
    ArrayAgg = None


class OrmAggregateField(OrmBaseField):
    def __init__(self, base_type, name, agg_func, type_):
        super().__init__(
            base_type.name, name, name.replace("_", " "), type_=type_, concrete=True
        )
        self.base_type = base_type
        self.agg_func = agg_func

    def bind(self, previous):
        assert previous
        assert previous.type_ == self.base_type
        full_path = previous.full_path + [self.name]
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=[annotation_path(full_path)],
            aggregate_clause=self.agg_func(previous.queryset_path_str),
            having=True,
        )


TYPE_AGGREGATES = {type_: [] for type_ in TYPES.values()}

for type_ in TYPES.values():
    if type_ != BooleanType:
        TYPE_AGGREGATES[type_].append(
            ("count", lambda x: models.Count(x, distinct=True), NumberType)
        )

TYPE_AGGREGATES[NumberType].extend(
    [
        ("average", models.Avg, NumberType),
        ("max", models.Max, NumberType),
        ("min", models.Min, NumberType),
        ("std_dev", models.StdDev, NumberType),
        ("sum", models.Sum, NumberType),
        ("variance", models.Variance, NumberType),
    ]
)

TYPE_AGGREGATES[DateTimeType].extend(
    [("max", models.Max, DateTimeType), ("min", models.Min, DateTimeType)]
)

TYPE_AGGREGATES[DateType].extend(
    [("max", models.Max, DateType), ("min", models.Min, DateType)]
)

TYPE_AGGREGATES[DurationType].extend(
    [
        ("average", lambda x: models.Avg(_CastDuration(x)), DurationType),
        ("max", models.Max, DurationType),
        ("min", models.Min, DurationType),
        ("sum", lambda x: models.Sum(_CastDuration(x)), DurationType),
    ]
)

TYPE_AGGREGATES[BooleanType].extend(
    [
        (
            "average",
            lambda x: models.Avg(Cast(x, output_field=IntegerField())),
            NumberType,
        ),
        ("sum", lambda x: models.Sum(Cast(x, output_field=IntegerField())), NumberType),
    ]
)

if "postgresql" in settings.DATABASES["default"]["ENGINE"]:
    for array_type in ArrayTypeMixin.__subclasses__():
        if array_type.raw_type is None:
            TYPE_AGGREGATES[array_type.element_type].append(
                (
                    "all",
                    lambda x: ArrayAgg(x, default=Value([]), distinct=True, ordering=x),
                    array_type,
                )
            )


class _CastDuration(Cast):
    def __init__(self, expression):
        super().__init__(expression, output_field=DurationField())

    def as_mysql(self, compiler, connection, **extra_context):
        # https://github.com/django/django/pull/13398
        template = "%(function)s(%(expressions)s AS signed integer)"
        return self.as_sql(compiler, connection, template=template, **extra_context)


def get_aggregates_for_type(type_):
    return {
        aggregate: OrmAggregateField(type_, aggregate, func, res_type)
        for aggregate, func, res_type in TYPE_AGGREGATES[type_]
    }
