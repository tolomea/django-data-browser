import json
from functools import lru_cache

import dateutil.parser
from django.conf import settings
from django.utils import dateparse, html, timezone

from .common import all_subclasses, get_optimal_decimal_places

ASC, DSC = "asc", "dsc"


class TypeMeta(type):
    def __repr__(cls):
        return cls.__name__

    @property
    def default_lookup(cls):
        lookups = cls.lookups
        return list(lookups)[0] if lookups else None

    @property
    def lookups(cls):
        return {name: type_.name for name, type_ in cls._lookups().items()}

    @property
    def name(cls):
        name = cls.__name__.lower()
        assert name.endswith("type")
        return name[: -len("type")]


class BaseType(metaclass=TypeMeta):
    default_value = None
    default_sort = None

    def __init__(self):
        assert False

    @staticmethod
    def _lookups():
        return {}

    @staticmethod
    def get_formatter(choices):
        assert not choices
        return lambda value: value

    @staticmethod
    def _parse(value):
        return value

    @classmethod
    def parse(cls, lookup, value):
        lookups = cls.lookups
        if lookup not in lookups:
            return None, f"Bad lookup '{lookup}' expected {lookups}"
        else:
            type_ = TYPES[lookups[lookup]]
            try:
                return type_._parse(value), None
            except Exception as e:
                err_message = str(e) if str(e) else repr(e)
                return None, err_message

    @staticmethod
    def get_format_hints(name, data):
        return {}


class StringType(BaseType):
    default_value = ""

    @staticmethod
    def _lookups():
        return {
            "equals": StringType,
            "contains": StringType,
            "starts_with": StringType,
            "ends_with": StringType,
            "regex": RegexType,
            "not_equals": StringType,
            "not_contains": StringType,
            "not_starts_with": StringType,
            "not_ends_with": StringType,
            "not_regex": RegexType,
            "is_null": BooleanType,
        }


class ChoiceTypeMixin:
    default_value = None

    @staticmethod
    def get_formatter(choices):
        assert choices
        choices = dict(choices)
        choices[None] = None
        return lambda value: choices.get(value, value)


class StringChoiceType(ChoiceTypeMixin, BaseType):
    @staticmethod
    def _lookups():
        return {
            **StringType._lookups(),
            "equals": StringChoiceType,
            "not_equals": StringChoiceType,
        }


class ArrayTypeMixin:
    default_value = None

    @staticmethod
    def get_formatter(choices):  # pragma: postgres
        if choices:
            choices = dict(choices)
            choices[None] = None
            return (
                lambda value: None
                if value is None
                else ", ".join(str(choices.get(v, v)) for v in value)
            )
        return lambda value: None if value is None else ", ".join(str(v) for v in value)


class StringArrayType(ArrayTypeMixin, BaseType):
    @staticmethod
    def _lookups():
        return {
            "contains": StringChoiceType,
            "length": NumberType,
            "not_contains": StringChoiceType,
            "not_length": NumberType,
            "is_null": BooleanType,
        }


class RegexType(BaseType):
    default_value = ".*"

    @staticmethod
    @lru_cache(maxsize=None)
    def _parse(value):
        from django.contrib.contenttypes.models import ContentType
        from django.db.transaction import atomic

        # this is dirty
        # we need to check if the regex is going to cause a db exception
        # and not kill any in progress transaction as we check
        with atomic():
            list(ContentType.objects.filter(model__regex=value))
        return value


class NumberType(BaseType):
    default_value = 0

    @staticmethod
    def _lookups():
        return {
            "equals": NumberType,
            "not_equals": NumberType,
            "gt": NumberType,
            "gte": NumberType,
            "lt": NumberType,
            "lte": NumberType,
            "is_null": BooleanType,
        }

    @staticmethod
    def get_formatter(choices):
        assert not choices
        return lambda value: None if value is None else float(value)

    @staticmethod
    def _parse(value):
        return float(value)

    @staticmethod
    def get_format_hints(name, data):
        # we add . here so there is always at least one .
        nums = [
            row[name] for row in data if row and row[name] and abs(row[name] > 0.0001)
        ]
        return {
            "decimalPlaces": get_optimal_decimal_places(nums),
            "significantFigures": 3,
            "lowCutOff": 0.0001,
            "highCutOff": 1e10,
        }


class NumberChoiceType(ChoiceTypeMixin, BaseType):
    @staticmethod
    def _lookups():
        return {
            **NumberType._lookups(),
            "equals": NumberChoiceType,
            "not_equals": NumberChoiceType,
        }


class NumberArrayType(ArrayTypeMixin, BaseType):
    @staticmethod
    def _lookups():
        return {
            "contains": NumberChoiceType,
            "length": NumberType,
            "not_contains": NumberChoiceType,
            "not_length": NumberType,
            "is_null": BooleanType,
        }


class YearType(NumberType):
    default_value = timezone.now().year
    default_sort = ASC

    @staticmethod
    def _lookups():
        return {
            "equals": YearType,
            "not_equals": YearType,
            "gt": YearType,
            "gte": YearType,
            "lt": YearType,
            "lte": YearType,
            "is_null": BooleanType,
        }

    @staticmethod
    def _parse(value):
        res = int(value)
        if res <= 1:
            raise Exception("Years must be > 1")
        return res


class DurationType(BaseType):
    default_value = ""

    @staticmethod
    def _lookups():
        return {
            "equals": DurationType,
            "not_equals": DurationType,
            "gt": DurationType,
            "gte": DurationType,
            "lt": DurationType,
            "lte": DurationType,
            "is_null": BooleanType,
        }

    @staticmethod
    def _parse(value):
        if value.count(":") == 1:
            value += ":0"

        res = dateparse.parse_duration(value)
        assert res is not None, "Duration value should be 'DD HH:MM:SS'"
        return res

    @staticmethod
    def get_formatter(choices):
        assert not choices
        return lambda value: None if value is None else str(value)


class DateTypeMixin:
    default_sort = ASC

    @classmethod
    def _lookups(cls):
        return {
            "equals": cls,
            "not_equals": cls,
            "gt": cls,
            "gte": cls,
            "lt": cls,
            "lte": cls,
            "is_null": BooleanType,
        }

    @classmethod
    def _parse(cls, value):
        res = {
            dateutil.parser.parse(value, dayfirst=False, yearfirst=False),
            dateutil.parser.parse(value, dayfirst=True, yearfirst=False),
            dateutil.parser.parse(value, dayfirst=False, yearfirst=True),
        }
        assert len(res) == 1, "Ambiguous value"
        return timezone.make_aware(res.pop())


class DateTimeType(DateTypeMixin, BaseType):
    default_value = "now"

    @classmethod
    def _parse(cls, value):
        if value.lower().strip() == "now":
            return timezone.now()
        return super()._parse(value)

    @staticmethod
    def get_formatter(choices):
        assert not choices
        if settings.USE_TZ:
            return (
                lambda value: None if value is None else str(timezone.make_naive(value))
            )
        else:
            return lambda value: None if value is None else str(value)


class DateType(DateTypeMixin, BaseType):
    default_value = "today"

    @classmethod
    def _parse(cls, value):
        if value.lower().strip() == "today":
            return timezone.now().date()
        return super()._parse(value).date()

    @staticmethod
    def get_formatter(choices):
        assert not choices
        return lambda value: None if value is None else str(value)


class WeekDayType(BaseType):
    default_value = "Monday"
    default_sort = ASC

    @staticmethod
    def _lookups():
        return {"equals": WeekDayType, "not_equals": WeekDayType}

    _days = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]

    @classmethod
    def get_formatter(cls, value, choices=None):
        assert not choices
        return lambda value: None if value is None else cls._days[value - 1]

    @classmethod
    def _parse(cls, value):
        for i, v in enumerate(cls._days):
            if v.lower()[:3] == value.lower()[:3]:
                return i + 1
        raise Exception("not a day of the week")


class MonthType(BaseType):
    default_value = "January"
    default_sort = ASC

    @staticmethod
    def _lookups():
        return {"equals": MonthType, "not_equals": MonthType}

    _months = [
        "January",
        "Feburary",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    @classmethod
    def get_formatter(cls, value, choices=None):
        assert not choices
        return lambda value: None if value is None else cls._months[value - 1]

    @classmethod
    def _parse(cls, value):
        for i, v in enumerate(cls._months):
            if v.lower()[:3] == value.lower()[:3]:
                return i + 1
        raise Exception("not a month")


class HTMLType(StringType):
    @staticmethod
    def get_formatter(value, choices=None):
        assert not choices
        return lambda value: None if value is None else html.conditional_escape(value)


class BooleanType(BaseType):
    default_value = True

    @staticmethod
    def _lookups():
        return {
            "equals": BooleanType,
            "not_equals": BooleanType,
            "is_null": BooleanType,
        }

    @staticmethod
    def _parse(value):
        value = value.lower()
        if value == "true":
            return True
        elif value == "false":
            return False
        else:
            raise ValueError("Expected 'true' or 'false'")

    @staticmethod
    def get_formatter(value, choices=None):
        assert not choices
        return lambda value: None if value is None else bool(value)


class IsNullType(BooleanType):
    default_value = True

    @staticmethod
    def _lookups():
        return {"equals": BooleanType}

    @staticmethod
    def get_formatter(choices):
        assert not choices
        return lambda value: None if value is None else "IsNull" if value else "NotNull"


class UnknownType(BaseType):
    @staticmethod
    def get_formatter(choices):
        assert not choices
        return lambda value: None if value is None else str(value)

    @staticmethod
    def _lookups():
        return {"is_null": BooleanType}


class JSONFieldType(BaseType):
    default_value = "|"

    @staticmethod
    def _parse(value):
        value = value.strip()
        if "|" not in value:
            raise ValueError("Missing seperator '|'")
        field, value = value.split("|", 1)
        if not field:
            raise ValueError("Invalid field name")
        if value.startswith("{") or value.startswith("["):
            raise ValueError("Not a JSON primitive")
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            raise ValueError("Not a JSON primitive")
        return [field, value]


class JSONType(BaseType):
    @staticmethod
    def _lookups():
        return {
            "is_null": BooleanType,
            "has_key": StringType,
            "field_equals": JSONFieldType,
            "not_has_key": StringType,
            "not_field_equals": JSONFieldType,
        }


TYPES = {cls.name: cls for cls in all_subclasses(BaseType)}
