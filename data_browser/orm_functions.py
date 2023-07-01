from django.db.models import BooleanField, DateField, ExpressionWrapper, Q, functions

from .orm_fields import OrmBaseField, OrmBoundField
from .types import (
    ARRAY_TYPES,
    ASC,
    TYPES,
    ArrayTypeMixin,
    DateTimeType,
    DateType,
    IsNullType,
    NumberChoiceType,
    NumberType,
    StringType,
)
from .util import annotation_path

try:
    from django.contrib.postgres.fields.array import ArrayLenTransform
except ModuleNotFoundError:  # pragma: no cover
    ArrayLenTransform = None


_month_choices = [
    (1, "January"),
    (2, "February"),
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


def IsNull(field_name):
    return ExpressionWrapper(Q(**{field_name: None}), output_field=BooleanField())


class OrmBoundFunctionField(OrmBoundField):
    def _annotate(self, qs, debug=False):
        func = _get_django_function(self.previous.type_, self.name, qs)[0](
            self.previous.queryset_path_str
        )
        return self._annotate_qs(qs, func)

    def parse_lookup(self, lookup, value):
        parsed, error_message = super().parse_lookup(lookup, value)
        if (
            self.name in ["year", "iso_year"]
            and parsed is not None
            and lookup != "is_null"
        ):
            if parsed < 2:
                error_message = "Can't filter to years less than 2"
            if parsed > 9998:
                error_message = "Can't filter to years greater than 9998"
        return parsed, error_message


class OrmFunctionField(OrmBaseField):
    def __init__(self, base_type, name, type_, choices, default_sort, format_hints):
        super().__init__(
            base_type.name,
            name,
            name.replace("_", " "),
            type_=type_,
            concrete=True,
            can_pivot=True,
            choices=choices,
            default_sort=default_sort,
            format_hints=format_hints,
        )
        self.base_type = base_type

    def bind(self, previous):
        assert previous
        assert previous.type_ == self.base_type
        full_path = previous.full_path + [self.name]
        return OrmBoundFunctionField(
            field=self,
            previous=previous,
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=[annotation_path(full_path)],
            filter_=True,
        )


def _get_django_function(type_, name, qs):
    if issubclass(type_, ArrayTypeMixin) and name == "length":
        return (ArrayLenTransform, NumberType, (), None, {})

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
    return mapping[name]


TYPE_FUNCTIONS = {type_: [] for type_ in TYPES.values()}

for type_ in TYPES.values():
    TYPE_FUNCTIONS[type_].append("is_null")

for array_type in ARRAY_TYPES.values():
    TYPE_FUNCTIONS[array_type].append("length")

for type_ in [DateType, DateTimeType]:
    TYPE_FUNCTIONS[type_].append("year")
    TYPE_FUNCTIONS[type_].append("quarter")
    TYPE_FUNCTIONS[type_].append("month")
    TYPE_FUNCTIONS[type_].append("day")
    TYPE_FUNCTIONS[type_].append("week_day")
    TYPE_FUNCTIONS[type_].append("month_start")
    TYPE_FUNCTIONS[type_].append("iso_year")
    TYPE_FUNCTIONS[type_].append("iso_week")
    TYPE_FUNCTIONS[type_].append("week_start")

TYPE_FUNCTIONS[DateTimeType].append("hour")
TYPE_FUNCTIONS[DateTimeType].append("minute")
TYPE_FUNCTIONS[DateTimeType].append("second")
TYPE_FUNCTIONS[DateTimeType].append("date")

TYPE_FUNCTIONS[StringType].append("length")


def get_functions_for_type(type_):
    funcs = TYPE_FUNCTIONS[type_]
    return {
        name: OrmFunctionField(
            type_, name, *_get_django_function(type_, name, None)[1:]
        )
        for name in funcs
    }
