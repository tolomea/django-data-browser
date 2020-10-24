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
    choices = ()

    def __init__(self):
        assert False

    @staticmethod
    def _lookups():
        return {}

    @staticmethod
    def _get_formatter(choices):
        assert not choices
        return lambda value: value

    @classmethod
    def get_formatter(cls, choices):
        return cls._get_formatter(choices)

    @staticmethod
    def _parse(value, choices):
        assert not choices
        return value

    @classmethod
    def parse(cls, lookup, value, choices):
        lookups = cls.lookups
        if lookup not in lookups:
            return None, f"Bad lookup '{lookup}' expected {lookups}"
        else:
            type_ = TYPES[lookups[lookup]]
            try:
                return type_._parse(value, choices), None
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
    def _get_formatter(choices):
        assert not choices
        return lambda value: None if value is None else float(value)

    @staticmethod
    def _parse(value, choices):
        assert not choices
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


class RegexType(BaseType):
    default_value = ".*"

    @staticmethod
    @lru_cache(maxsize=None)
    def _parse(value, choices):
        assert not choices
        from django.contrib.contenttypes.models import ContentType
        from django.db.transaction import atomic

        # this is dirty
        # we need to check if the regex is going to cause a db exception
        # and not kill any in progress transaction as we check
        with atomic():
            list(ContentType.objects.filter(model__regex=value))
        return value


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
    def _parse(value, choices):
        assert not choices
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
    def _parse(value, choices):
        assert not choices
        if value.count(":") == 1:
            value += ":0"

        res = dateparse.parse_duration(value)
        assert res is not None, "Duration value should be 'DD HH:MM:SS'"
        return res

    @staticmethod
    def _get_formatter(choices):
        assert not choices
        return lambda value: None if value is None else str(value)


class DateTimeType(BaseType):
    default_value = "now"
    default_sort = ASC

    @staticmethod
    def _lookups():
        return {
            "equals": DateTimeType,
            "not_equals": DateTimeType,
            "gt": DateTimeType,
            "gte": DateTimeType,
            "lt": DateTimeType,
            "lte": DateTimeType,
            "is_null": BooleanType,
        }

    @staticmethod
    def _parse(value, choices):
        assert not choices
        if value.lower().strip() == "now":
            return timezone.now()
        return timezone.make_aware(dateutil.parser.parse(value))

    @staticmethod
    def _get_formatter(choices):
        assert not choices
        if settings.USE_TZ:
            return (
                lambda value: None if value is None else str(timezone.make_naive(value))
            )
        else:
            return lambda value: None if value is None else str(value)


class DateType(BaseType):
    default_value = "today"
    default_sort = ASC

    @staticmethod
    def _lookups():
        return {
            "equals": DateType,
            "not_equals": DateType,
            "gt": DateType,
            "gte": DateType,
            "lt": DateType,
            "lte": DateType,
            "is_null": BooleanType,
        }

    @staticmethod
    def _parse(value, choices):
        assert not choices
        if value.lower().strip() == "today":
            return timezone.now().date()
        return timezone.make_aware(dateutil.parser.parse(value)).date()

    @staticmethod
    def _get_formatter(choices):
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
    def _get_formatter(cls, choices):
        assert not choices
        return lambda value: None if value is None else cls._days[value - 1]

    @classmethod
    def _parse(cls, value, choices):
        assert not choices
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
    def _get_formatter(cls, choices):
        assert not choices
        return lambda value: None if value is None else cls._months[value - 1]

    @classmethod
    def _parse(cls, value, choices):
        assert not choices
        for i, v in enumerate(cls._months):
            if v.lower()[:3] == value.lower()[:3]:
                return i + 1
        raise Exception("not a month")


class HTMLType(StringType):
    @staticmethod
    def _get_formatter(choices):
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
    def _parse(value, choices):
        assert not choices
        value = value.lower()
        if value == "true":
            return True
        elif value == "false":
            return False
        else:
            raise ValueError("Expected 'true' or 'false'")

    @staticmethod
    def _get_formatter(choices):
        assert not choices
        return lambda value: None if value is None else bool(value)


class UnknownType(BaseType):
    @staticmethod
    def _get_formatter(choices):
        assert not choices
        return lambda value: None if value is None else str(value)

    @staticmethod
    def _lookups():
        return {"is_null": BooleanType}


class JSONFieldType(BaseType):
    default_value = "|"

    @staticmethod
    def _parse(value, choices):
        assert not choices
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


class ChoiceTypeMixin:
    default_value = None

    @classmethod
    def _get_formatter(cls, choices):
        if cls.choices:
            choices = cls.choices

        assert choices
        choices = dict(choices)
        choices[None] = None
        return lambda value: choices.get(value, value)

    @classmethod
    def _parse(cls, value, choices):
        if cls.choices:
            choices = cls.choices

        assert choices
        choices = {v: k for k, v in choices}
        return choices[value]

    @staticmethod
    def _lookups():
        return {
            "equals": StringChoiceType,
            "not_equals": StringChoiceType,
            "is_null": BooleanType,
        }


class StringChoiceType(ChoiceTypeMixin, BaseType):
    pass


class NumberChoiceType(ChoiceTypeMixin, BaseType):
    pass


class IsNullType(ChoiceTypeMixin, BaseType):
    choices = [(True, "IsNull"), (False, "NotNull")]
    default_value = choices[0][1]

    @staticmethod
    def _lookups():
        return {"equals": IsNullType}


class ArrayTypeMixin:
    default_value = None

    @staticmethod
    def _get_formatter(choices):  # pragma: postgres
        if choices:
            choices = dict(choices)
            choices[None] = None
            return (
                lambda value: None
                if value is None
                else ", ".join(str(choices.get(v, v)) for v in value)
            )
        return lambda value: None if value is None else ", ".join(str(v) for v in value)

    @classmethod
    def _lookups(cls):
        return {
            "contains": cls.base_type,
            "length": NumberType,
            "not_contains": cls.base_type,
            "not_length": NumberType,
            "is_null": BooleanType,
        }


class StringArrayType(ArrayTypeMixin, BaseType):
    base_type = StringType


class NumberArrayType(ArrayTypeMixin, BaseType):
    base_type = NumberType


class StringChoiceArrayType(ArrayTypeMixin, BaseType):
    base_type = StringChoiceType


class NumberChoiceArrayType(ArrayTypeMixin, BaseType):
    base_type = NumberChoiceType


TYPES = {cls.name: cls for cls in all_subclasses(BaseType)}
