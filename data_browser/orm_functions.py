from dataclasses import dataclass
from dataclasses import field
from typing import Optional

from django.db.models import BooleanField
from django.db.models import DateField
from django.db.models import ExpressionWrapper
from django.db.models import Q
from django.db.models import functions

from data_browser.orm_fields import OrmBaseField
from data_browser.orm_fields import OrmBoundField
from data_browser.types import ARRAY_TYPES
from data_browser.types import ASC
from data_browser.types import TYPES
from data_browser.types import BaseType
from data_browser.types import DateTimeType
from data_browser.types import DateType
from data_browser.types import IsNullType
from data_browser.types import NumberChoiceType
from data_browser.types import NumberType
from data_browser.types import StringType
from data_browser.util import annotation_path

try:
    from django.contrib.postgres.fields.array import ArrayLenTransform
except ModuleNotFoundError:  # pragma: no cover
    ArrayLenTransform = None


class OrmBoundFunctionField(OrmBoundField):
    def __init__(self, *args, func, **kwargs):
        super().__init__(*args, **kwargs)
        self.func = func

    def _annotate(self, qs, debug=False):
        return self._annotate_qs(qs, self.func(self.previous.queryset_path_str))

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
    def __init__(self, base_type, name, func):
        super().__init__(
            base_type.name,
            name,
            name.replace("_", " "),
            type_=func.type_,
            concrete=True,
            can_pivot=True,
            choices=func.choices,
            default_sort=func.default_sort,
            format_hints=func.format_hints,
        )
        self.base_type = base_type
        self.func = func.func

    def bind(self, previous):
        assert previous
        assert previous.type_ == self.base_type
        full_path = previous.full_path + [self.name]
        return OrmBoundFunctionField(
            field=self,
            previous=previous,
            full_path=full_path,
            verbose_path=previous.verbose_path + [self.verbose_name],
            queryset_path=[annotation_path(full_path)],
            filter_=True,
            func=self.func,
        )


def IsNull(field_name):
    return ExpressionWrapper(Q(**{field_name: None}), output_field=BooleanField())


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


@dataclass
class Func:
    func: callable
    type_: BaseType
    choices: tuple = ()
    default_sort: Optional[str] = ASC
    format_hints: dict = field(default_factory=dict)


TYPE_FUNCTIONS = {type_: {} for type_ in TYPES.values()}

for type_ in TYPES.values():
    TYPE_FUNCTIONS[type_]["is_null"] = Func(IsNull, IsNullType, default_sort=None)

for array_type in ARRAY_TYPES.values():
    TYPE_FUNCTIONS[array_type]["length"] = Func(
        ArrayLenTransform, NumberType, default_sort=None
    )

for type_ in [DateType, DateTimeType]:
    TYPE_FUNCTIONS[type_]["year"] = Func(
        functions.ExtractYear, NumberType, format_hints={"useGrouping": False}
    )
    TYPE_FUNCTIONS[type_]["quarter"] = Func(functions.ExtractQuarter, NumberType)
    TYPE_FUNCTIONS[type_]["month"] = Func(
        functions.ExtractMonth, NumberChoiceType, choices=_month_choices
    )
    TYPE_FUNCTIONS[type_]["day"] = Func(functions.ExtractDay, NumberType)
    TYPE_FUNCTIONS[type_]["week_day"] = Func(
        functions.ExtractWeekDay, NumberChoiceType, choices=_weekday_choices
    )
    TYPE_FUNCTIONS[type_]["month_start"] = Func(
        lambda x: functions.TruncMonth(x, DateField()), DateType
    )
    TYPE_FUNCTIONS[type_]["iso_year"] = Func(functions.ExtractIsoYear, NumberType)
    TYPE_FUNCTIONS[type_]["iso_week"] = Func(functions.ExtractWeek, NumberType)
    TYPE_FUNCTIONS[type_]["week_start"] = Func(
        lambda x: functions.TruncWeek(x, DateField()), DateType
    )

TYPE_FUNCTIONS[DateTimeType]["hour"] = Func(functions.ExtractHour, NumberType)
TYPE_FUNCTIONS[DateTimeType]["minute"] = Func(functions.ExtractMinute, NumberType)
TYPE_FUNCTIONS[DateTimeType]["second"] = Func(functions.ExtractSecond, NumberType)
TYPE_FUNCTIONS[DateTimeType]["date"] = Func(functions.TruncDate, DateType)

TYPE_FUNCTIONS[StringType]["length"] = Func(
    functions.Length, NumberType, default_sort=None
)


def get_functions_for_type(type_):
    return {
        name: OrmFunctionField(type_, name, func)
        for name, func in TYPE_FUNCTIONS[type_].items()
    }
