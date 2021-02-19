from collections import defaultdict

import django
from django.db.models import (
    BooleanField,
    DateField,
    ExpressionWrapper,
    OuterRef,
    Q,
    Subquery,
    functions,
)

from .orm_fields import OrmBaseField, OrmBoundField
from .types import (
    ASC,
    DateTimeType,
    DateType,
    IsNullType,
    NumberChoiceType,
    NumberType,
    StringType,
)
from .util import s

_DATE_FUNCTIONS = [
    "is_null",
    "year",
    "quarter",
    "month",
    "day",
    "week_day",
    "month_start",
    "iso_year",
    "iso_week",
    "week_start",
]


_TYPE_FUNCTIONS = defaultdict(
    lambda: ["is_null"],
    {
        DateType: _DATE_FUNCTIONS,
        DateTimeType: _DATE_FUNCTIONS + ["hour", "minute", "second", "date"],
        StringType: ["is_null", "length"],
    },
)


_month_choices = [
    (1, "January"),
    (2, "Feburary"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December"),
]


_weekday_choices = [
    (1, "Sunday"),
    (2, "Monday"),
    (3, "Tuesday"),
    (4, "Wednesday"),
    (5, "Thursday"),
    (6, "Friday"),
    (7, "Saturday"),
]


def _get_django_function(name, qs):
    def IsNull(field_name):
        # https://code.djangoproject.com/ticket/32200
        if django.VERSION[:3] == (3, 1, 3):  # pragma: django != 3.1.3
            return Subquery(
                qs.annotate(
                    ddb_is_null=ExpressionWrapper(
                        Q(**{field_name: None}), output_field=BooleanField()
                    )
                )
                .filter(pk=OuterRef("pk"))
                .values("ddb_is_null")[:1],
                output_field=BooleanField(),
            )
        else:
            return ExpressionWrapper(
                Q(**{field_name: None}), output_field=BooleanField()
            )

    mapping = {
        "year": (functions.ExtractYear, NumberType, (), ASC, {"useGrouping": False}),
        "quarter": (functions.ExtractQuarter, NumberType, (), ASC, {}),
        "month": (functions.ExtractMonth, NumberChoiceType, _month_choices, ASC, {}),
        "month_start": (
            lambda x: functions.TruncMonth(x, DateField()),
            DateType,
            (),
            ASC,
            {},
        ),
        "day": (functions.ExtractDay, NumberType, (), ASC, {}),
        "week_day": (
            functions.ExtractWeekDay,
            NumberChoiceType,
            _weekday_choices,
            ASC,
            {},
        ),
        "hour": (functions.ExtractHour, NumberType, (), ASC, {}),
        "minute": (functions.ExtractMinute, NumberType, (), ASC, {}),
        "second": (functions.ExtractSecond, NumberType, (), ASC, {}),
        "date": (functions.TruncDate, DateType, (), ASC, {}),
        "is_null": (IsNull, IsNullType, (), None, {}),
        "length": (functions.Length, NumberType, (), None, {}),
    }
    mapping.update(
        {
            "iso_year": (functions.ExtractIsoYear, NumberType, (), ASC, {}),
            "iso_week": (functions.ExtractWeek, NumberType, (), ASC, {}),
            "week_start": (
                lambda x: functions.TruncWeek(x, DateField()),
                DateType,
                (),
                ASC,
                {},
            ),
        }
    )
    return mapping[name]


class OrmBoundFunctionField(OrmBoundField):
    def _annotate(self, request, qs):
        func = _get_django_function(self.name, qs)[0](s(self.previous.queryset_path))
        return qs.annotate(**{s(self.queryset_path): func})

    def parse_lookup(self, lookup, value):
        parsed, err_message = super().parse_lookup(lookup, value)
        if (
            self.name in ["year", "iso_year"]
            and parsed is not None
            and lookup != "is_null"
        ):
            if parsed < 2:
                err_message = "Can't filter to years less than 2"
            if parsed > 9998:
                err_message = "Can't filter to years greater than 9998"
        return parsed, err_message


class OrmFunctionField(OrmBaseField):
    def __init__(self, model_name, name, type_, choices, default_sort, format_hints):
        super().__init__(
            model_name,
            name,
            name.replace("_", " "),
            type_=type_,
            concrete=True,
            can_pivot=True,
            choices=choices,
            default_sort=default_sort,
            format_hints=format_hints,
        )

    def bind(self, previous):
        assert previous
        return OrmBoundFunctionField(
            field=self,
            previous=previous,
            full_path=previous.full_path + [self.name],
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=previous.queryset_path + [self.name],
            filter_=True,
        )


def get_functions_for_type(type_):
    return {
        func: OrmFunctionField(type_.name, func, *_get_django_function(func, None)[1:])
        for func in _TYPE_FUNCTIONS[type_]
    }
