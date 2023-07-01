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
        TYPE_AGGREGATES[type_].append(("count", NumberType))

TYPE_AGGREGATES[NumberType].extend(
    [
        ("average", NumberType),
        ("max", NumberType),
        ("min", NumberType),
        ("std_dev", NumberType),
        ("sum", NumberType),
        ("variance", NumberType),
    ]
)

TYPE_AGGREGATES[DateTimeType].extend([("max", DateTimeType), ("min", DateTimeType)])

TYPE_AGGREGATES[DateType].extend([("max", DateType), ("min", DateType)])

TYPE_AGGREGATES[DurationType].extend(
    [
        ("average", DurationType),
        ("max", DurationType),
        ("min", DurationType),
        ("sum", DurationType),
    ]
)

TYPE_AGGREGATES[BooleanType].extend([("average", NumberType), ("sum", NumberType)])

if "postgresql" in settings.DATABASES["default"]["ENGINE"]:
    for array_type in ArrayTypeMixin.__subclasses__():
        if array_type.raw_type is None:
            TYPE_AGGREGATES[array_type.element_type].append(("all", array_type))


class _CastDuration(Cast):
    def __init__(self, expression):
        super().__init__(expression, output_field=DurationField())

    def as_mysql(self, compiler, connection, **extra_context):
        # https://github.com/django/django/pull/13398
        template = "%(function)s(%(expressions)s AS signed integer)"
        return self.as_sql(compiler, connection, template=template, **extra_context)


def _get_django_aggregate(field_type, name):
    if name == "all":
        return lambda x: ArrayAgg(x, default=Value([]), distinct=True, ordering=x)

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
            "average": models.Avg,
            "count": lambda x: models.Count(x, distinct=True),
            "max": models.Max,
            "min": models.Min,
            "std_dev": models.StdDev,
            "sum": models.Sum,
            "variance": models.Variance,
        }[name]


def get_aggregates_for_type(type_):
    return {
        aggregate: OrmAggregateField(
            type_, aggregate, _get_django_aggregate(type_, aggregate), res_type
        )
        for aggregate, res_type in TYPE_AGGREGATES[type_]
    }
