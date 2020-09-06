import json
from functools import lru_cache

import dateutil.parser
from django.utils import timezone

from .common import all_subclasses, get_optimal_decimal_places


class TypeMeta(type):
    def __repr__(cls):
        return cls.__name__

    @property
    def default_lookup(cls):
        return list(cls.lookups)[0] if cls.lookups else None

    @property
    def name(cls):
        name = cls.__name__.lower()
        assert name.endswith("type")
        return name[: -len("type")]


class BaseType(metaclass=TypeMeta):
    default_value = None
    lookups = {}

    def __init__(self):
        assert False

    @staticmethod
    def format(value, choices=None):
        assert not choices
        return value

    @staticmethod
    def _parse(value):
        return value

    @classmethod
    def parse(cls, lookup, value):
        if lookup not in cls.lookups:
            return None, f"Bad lookup '{lookup}' expected {cls.lookups}"
        else:
            type_ = TYPES[cls.lookups[lookup]]
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
    lookups = {
        "equals": "string",
        "contains": "string",
        "starts_with": "string",
        "ends_with": "string",
        "regex": "regex",
        "not_equals": "string",
        "not_contains": "string",
        "not_starts_with": "string",
        "not_ends_with": "string",
        "not_regex": "regex",
        "is_null": "boolean",
    }


class ChoiceTypeMixin:
    default_value = None

    @staticmethod
    def format(value, choices=None):
        assert choices
        return dict(choices)[value] if value is not None else None


class StringChoiceType(ChoiceTypeMixin, BaseType):
    lookups = {
        **StringType.lookups,
        "equals": "stringchoice",
        "not_equals": "stringchoice",
    }


class ArrayTypeMixin:
    default_value = None

    @staticmethod
    def format(value, choices=None):  # pragma: postgres
        if choices:
            value = [dict(choices)[v] if v is not None else None for v in value]
        return ", ".join(str(v) for v in value)


class StringArrayType(ArrayTypeMixin, BaseType):
    lookups = {
        "contains": "stringchoice",
        "length": "number",
        "not_contains": "stringchoice",
        "not_length": "number",
        "is_null": "boolean",
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
    lookups = {
        "equals": "number",
        "not_equals": "number",
        "gt": "number",
        "gte": "number",
        "lt": "number",
        "lte": "number",
        "is_null": "boolean",
    }

    @staticmethod
    def format(value, choices=None):
        assert not choices
        return float(value) if value is not None else None

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
    lookups = {
        **NumberType.lookups,
        "equals": "numberchoice",
        "not_equals": "numberchoice",
    }


class NumberArrayType(ArrayTypeMixin, BaseType):
    lookups = {
        "contains": "numberchoice",
        "length": "number",
        "not_contains": "numberchoice",
        "not_length": "number",
        "is_null": "boolean",
    }


class YearType(NumberType):
    default_value = timezone.now().year
    lookups = {
        "equals": "year",
        "not_equals": "year",
        "gt": "year",
        "gte": "year",
        "lt": "year",
        "lte": "year",
        "is_null": "boolean",
    }

    @staticmethod
    def _parse(value):
        res = int(value)
        if res <= 1:
            raise Exception("Years must be > 1")
        return res


class DateTimeType(BaseType):
    default_value = "now"
    lookups = {
        "equals": "datetime",
        "not_equals": "datetime",
        "gt": "datetime",
        "gte": "datetime",
        "lt": "datetime",
        "lte": "datetime",
        "is_null": "boolean",
    }

    @staticmethod
    def _parse(value):
        if value.lower().strip() == "now":
            return timezone.now()
        return timezone.make_aware(dateutil.parser.parse(value))

    @staticmethod
    def format(value, choices=None):
        assert not choices
        return str(timezone.make_naive(value)) if value else None


class DateType(BaseType):
    default_value = "today"
    lookups = {
        "equals": "date",
        "not_equals": "date",
        "gt": "date",
        "gte": "date",
        "lt": "date",
        "lte": "date",
        "is_null": "boolean",
    }

    @staticmethod
    def _parse(value):
        if value.lower().strip() == "today":
            return timezone.now().date()
        return timezone.make_aware(dateutil.parser.parse(value)).date()

    @staticmethod
    def format(value, choices=None):
        assert not choices
        return str(value) if value else None


class WeekDayType(BaseType):
    default_value = "Monday"
    lookups = {"equals": "weekday", "not_equals": "weekday"}

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
    def format(cls, value, choices=None):
        assert not choices
        return cls._days[value - 1] if value else None

    @classmethod
    def _parse(cls, value):
        for i, v in enumerate(cls._days):
            if v.lower()[:3] == value.lower()[:3]:
                return i + 1
        raise Exception("not a day of the week")


class MonthType(BaseType):
    default_value = "January"
    lookups = {"equals": "month", "not_equals": "month"}

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
    def format(cls, value, choices=None):
        assert not choices
        return cls._months[value - 1] if value else None

    @classmethod
    def _parse(cls, value):
        for i, v in enumerate(cls._months):
            if v.lower()[:3] == value.lower()[:3]:
                return i + 1
        raise Exception("not a month")


class HTMLType(StringType):
    pass


class BooleanType(BaseType):
    default_value = True
    lookups = {"equals": "boolean", "not_equals": "boolean", "is_null": "boolean"}

    @staticmethod
    def _parse(value):
        value = value.lower()
        if value == "true":
            return True
        elif value == "false":
            return False
        else:
            raise ValueError("Expected 'true' or 'false'")


class IsNullType(BooleanType):
    default_value = True
    lookups = {"equals": "boolean"}

    @staticmethod
    def format(value, choices=None):
        assert not choices
        return "IsNull" if value else "NotNull"


class UnknownType(BaseType):
    @staticmethod
    def format(value, choices=None):
        assert not choices
        return str(value)

    lookups = {"is_null": "boolean"}


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
    lookups = {
        "is_null": "boolean",
        "has_key": "string",
        "field_equals": "jsonfield",
        "not_has_key": "string",
        "not_field_equals": "jsonfield",
    }


TYPES = {cls.name: cls for cls in all_subclasses(BaseType)}
