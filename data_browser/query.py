import urllib
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Optional, Sequence

import dateutil.parser
from django.urls import reverse
from django.utils import timezone

from .common import settings

ASC, DSC = "asc", "dsc"


@dataclass
class QueryField:
    path: str
    pivoted: bool = False
    direction: str = None
    priority: int = None

    def __post_init__(self):
        self.path = self.path.split("__")
        assert (self.direction is None) == (self.priority is None)


@dataclass
class QueryFilter:
    path: str
    lookup: str
    value: str

    def __post_init__(self):
        self.path = self.path.split("__")


def parse_sort(value, symbol, direction):
    path, priority = value.split(symbol)
    try:
        return path, direction, int(priority)
    except:  # noqa: E722  input sanitization
        return path, None, None


@dataclass
class Query:
    model_name: str
    fields: Sequence[QueryField]
    filters: Sequence[QueryFilter]
    limit: int = settings.DATA_BROWSER_DEFAULT_ROW_LIMIT

    @classmethod
    def from_request(cls, model_name, field_str, get_args):
        fields = []
        found_fields = set()
        for field in field_str.split(","):
            field = field.strip()
            if field:
                # pivot
                if field.startswith("&"):
                    field = field[1:]
                    pivoted = True
                else:
                    pivoted = False

                # sort
                if "+" in field:
                    path, direction, priority = parse_sort(field, "+", ASC)
                elif "-" in field:
                    path, direction, priority = parse_sort(field, "-", DSC)
                else:
                    path, direction, priority = field, None, None

                # collect
                if path not in found_fields:
                    found_fields.add(path)
                    fields.append(QueryField(path, pivoted, direction, priority))

        limit = settings.DATA_BROWSER_DEFAULT_ROW_LIMIT

        filters = []
        for path__lookup, values in dict(get_args).items():
            for value in values:
                if path__lookup == "limit":
                    limit = int(value)
                if "__" in path__lookup:
                    path, lookup = path__lookup.rsplit("__", 1)
                    filters.append(QueryFilter(path, lookup, value))

        return cls(model_name, fields, filters, limit)

    @property
    def _field_str(self):
        field_strs = []
        for field in self.fields:
            pivot = "&" if field.pivoted else ""
            direction = {ASC: "+", DSC: "-", None: ""}[field.direction]
            priority = str(field.priority) if field.direction else ""
            field_strs.append(f"{pivot}{'__'.join(field.path)}{direction}{priority}")
        return ",".join(field_strs)

    @property
    def _filter_fields(self):
        return [
            ("__".join(filter.path + [filter.lookup]), filter.value)
            for filter in self.filters
        ] + [("limit", self.limit)]

    def get_url(self, media):
        base_url = reverse(
            "data_browser:query",
            kwargs={
                "model_name": self.model_name,
                "fields": self._field_str,
                "media": media,
            },
        )
        params = urllib.parse.urlencode(
            self._filter_fields, quote_via=urllib.parse.quote_plus, doseq=True
        )
        return f"{base_url}?{params}"


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
    def format(value):
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
    def format(value):
        return float(value) if value is not None else None

    @staticmethod
    def _parse(value):
        return float(value)


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
    def format(value):
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
    def format(value):
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
    def format(cls, value):
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
    def format(cls, value):
        return cls._months[value - 1] if value else None

    @classmethod
    def _parse(cls, value):
        for i, v in enumerate(cls._months):
            if v.lower()[:3] == value.lower()[:3]:
                return i + 1
        raise Exception("not a month")


class HTMLType(BaseType):
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


def all_subclasses(cls):
    res = set()
    queue = {cls}
    while queue:
        cls = queue.pop()
        subs = set(cls.__subclasses__())
        queue.update(subs - res)
        res.update(subs)
    return res


TYPES = {cls.name: cls for cls in all_subclasses(BaseType)}


class BoundFieldMixin:
    @property
    def path(self):
        return self.orm_bound_field.full_path

    @property
    def pretty_path(self):
        return self.orm_bound_field.pretty_path

    @property
    def path_str(self):
        return self.orm_bound_field.path_str


@dataclass
class BoundFilter(BoundFieldMixin):
    orm_bound_field: Any
    lookup: str
    value: str

    @classmethod
    def bind(cls, orm_bound_field, query_filter):
        return cls(orm_bound_field, query_filter.lookup, query_filter.value)

    def __post_init__(self):
        self.parsed, self.err_message = self.orm_bound_field.type_.parse(
            self.lookup, self.value
        )
        self.is_valid = not self.err_message


@dataclass
class BoundField(BoundFieldMixin):
    orm_bound_field: Any
    pivoted: bool
    direction: Optional[str]
    priority: Optional[int]

    @classmethod
    def bind(cls, orm_bound_field, query_field):
        return cls(
            orm_bound_field,
            query_field.pivoted and orm_bound_field.can_pivot,
            query_field.direction if orm_bound_field.concrete else None,
            query_field.priority if orm_bound_field.concrete else None,
        )

    def unsorted(self):
        return self.__class__(self.orm_bound_field, self.pivoted, None, None)


def _orm_fields(fields):
    return [f.orm_bound_field for f in fields]


class BoundQuery:
    def __init__(self, model_name, fields, filters, limit):
        self.model_name = model_name
        self.fields = fields
        self.filters = filters
        self.limit = limit

    @classmethod
    def bind(cls, query, orm_models):
        def get_orm_field(parts):
            model_name = query.model_name
            orm_bound_field = None
            for part in parts:
                orm_field = orm_models[model_name].fields.get(part)
                if orm_field is None:
                    return None
                orm_bound_field = orm_field.bind(orm_bound_field)
                model_name = orm_field.rel_name
            if not orm_bound_field.type_:
                return None
            return orm_bound_field

        model_name = query.model_name

        fields = []
        for query_field in query.fields:
            orm_bound_field = get_orm_field(query_field.path)
            if orm_bound_field:
                fields.append(BoundField.bind(orm_bound_field, query_field))

        filters = []
        for query_filter in query.filters:
            orm_bound_field = get_orm_field(query_filter.path)
            if orm_bound_field and orm_bound_field.concrete:
                filters.append(BoundFilter.bind(orm_bound_field, query_filter))

        return cls(model_name, fields, filters, query.limit)

    @property
    def sort_fields(self):
        return sorted((f for f in self.fields if f.direction), key=lambda f: f.priority)

    @property
    def valid_filters(self):
        return [f for f in self.filters if f.is_valid]

    @property
    def col_fields(self):
        return [f for f in self.fields if f.pivoted]

    @property
    def row_fields(self):
        if self.col_fields:
            return [
                f for f in self.fields if f.orm_bound_field.can_pivot and not f.pivoted
            ]
        else:
            return self.fields

    @property
    def data_fields(self):
        if self.col_fields:
            return [f for f in self.fields if not f.orm_bound_field.can_pivot]
        else:
            return []

    @property
    def bound_fields(self):
        return _orm_fields(self.fields)

    @property
    def bound_filters(self):
        return _orm_fields(self.valid_filters)

    @property
    def bound_col_fields(self):
        return _orm_fields(self.col_fields)

    @property
    def bound_row_fields(self):
        return _orm_fields(self.row_fields)

    @property
    def bound_data_fields(self):
        return _orm_fields(self.data_fields)
