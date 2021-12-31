from collections import defaultdict

from django.conf import settings
from django.db import models
from django.db.models import DurationField, IntegerField, Value
from django.db.models.functions import Cast

from .orm_fields import OrmBaseField, OrmBoundField
from .types import (
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


_TYPE_AGGREGATES = defaultdict(
    lambda: [("count", NumberType)],
    {
        NumberType: [
            ("average", NumberType),
            ("count", NumberType),
            ("max", NumberType),
            ("min", NumberType),
            ("std_dev", NumberType),
            ("sum", NumberType),
            ("variance", NumberType),
        ],
        DateTimeType: [
            ("count", NumberType),
            ("max", DateTimeType),
            ("min", DateTimeType),
        ],
        DateType: [("count", NumberType), ("max", DateType), ("min", DateType)],
        DurationType: [
            ("count", NumberType),
            ("average", DurationType),
            ("sum", DurationType),
            ("max", DurationType),
            ("min", DurationType),
        ],
        BooleanType: [("average", NumberType), ("sum", NumberType)],
    },
)

if "postgresql" in settings.DATABASES["default"]["ENGINE"]:
    for array_type in ArrayTypeMixin.__subclasses__():
        if array_type.raw_type is None:
            _TYPE_AGGREGATES[array_type.element_type].append(("all", array_type))


class _CastDuration(Cast):
    def __init__(self, expression):
        super().__init__(expression, output_field=DurationField())

    def as_mysql(self, compiler, connection, **extra_context):
        # https://github.com/django/django/pull/13398
        template = "%(function)s(%(expressions)s AS signed integer)"
        return self.as_sql(compiler, connection, template=template, **extra_context)


def _get_django_aggregate(field_type, name):
    if field_type == BooleanType:
        return {
            "average": lambda x: models.Avg(Cast(x, output_field=IntegerField())),
            "sum": lambda x: models.Sum(Cast(x, output_field=IntegerField())),
        }[name]
    if field_type == DurationType and name in ["average", "sum"]:
        return {
            "average": lambda x: models.Avg(_CastDuration(x)),
            "sum": lambda x: models.Sum(_CastDuration(x)),
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
            "all": lambda x: ArrayAgg(x, default=Value([]), distinct=True, ordering=x),
        }[name]


class OrmAggregateField(OrmBaseField):
    def __init__(self, model_name, name, type_):
        super().__init__(
            model_name, name, name.replace("_", " "), type_=type_, concrete=True
        )

    def bind(self, previous):
        assert previous
        full_path = previous.full_path + [self.name]
        agg_func = _get_django_aggregate(previous.type_, self.name)
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=[annotation_path(full_path)],
            aggregate_clause=agg_func(previous.queryset_path_str),
            having=True,
        )


def get_aggregates_for_type(type_):
    return {
        aggregate: OrmAggregateField(type_.name, aggregate, res_type)
        for aggregate, res_type in _TYPE_AGGREGATES[type_]
    }
