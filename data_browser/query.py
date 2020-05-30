from __future__ import annotations

import urllib
from dataclasses import dataclass
from typing import Any, Optional, Sequence

import dateutil.parser
from django.urls import reverse
from django.utils import timezone

ASC, DSC = "asc", "dsc"


@dataclass
class QueryField:
    path: str
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

    @classmethod
    def from_request(cls, model_name, field_str, get_args):
        fields = []
        for field in field_str.split(","):
            field = field.strip()
            if field:
                if "+" in field:
                    path, direction, priority = parse_sort(field, "+", ASC)
                    fields.append(QueryField(path, direction, priority))
                elif "-" in field:
                    path, direction, priority = parse_sort(field, "-", DSC)
                    fields.append(QueryField(path, direction, priority))
                else:
                    fields.append(QueryField(field, None, None))

        filters = []
        for path__lookup, values in dict(get_args).items():
            for value in values:
                if "__" in path__lookup:
                    path, lookup = path__lookup.rsplit("__", 1)
                    filters.append(QueryFilter(path, lookup, value))

        return cls(model_name, fields, filters)

    @property
    def field_str(self):
        field_strs = []
        for field in self.fields:
            direction = {ASC: "+", DSC: "-", None: ""}[field.direction]
            priority = str(field.priority) if field.direction else ""
            field_strs.append(f"{'__'.join(field.path)}{direction}{priority}")
        return ",".join(field_strs)

    @property
    def filter_fields(self):
        return [
            ("__".join(filter.path + [filter.lookup]), filter.value)
            for filter in self.filters
        ]

    def get_url(self, media):
        base_url = reverse(
            "data_browser:query",
            kwargs={
                "model_name": self.model_name,
                "fields": self.field_str,
                "media": media,
            },
        )
        params = urllib.parse.urlencode(
            self.filter_fields, quote_via=urllib.parse.quote_plus, doseq=True
        )
        return f"{base_url}?{params}"


class MetaFieldType(type):
    def __repr__(cls):
        return cls.__name__

    @property
    def default_lookup(cls):
        return list(cls.lookups)[0] if cls.lookups else None

    @property
    def name(cls):
        name = cls.__name__.lower()
        assert name.endswith("fieldtype")
        return name[: -len("fieldtype")]


class FieldType(metaclass=MetaFieldType):
    def __init__(self):
        assert False

    @staticmethod
    def format(value):
        return value

    @staticmethod
    def parse(value):
        return value


class StringFieldType(FieldType):
    default_value = ""
    lookups = {
        "equals": "string",
        "contains": "string",
        "starts_with": "string",
        "ends_with": "string",
        "regex": "string",
        "not_equals": "string",
        "not_contains": "string",
        "not_starts_with": "string",
        "not_ends_with": "string",
        "not_regex": "string",
        "is_null": "boolean",
    }
    aggregates = ["count"]


class NumberFieldType(FieldType):
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
    aggregates = ["average", "count", "max", "min", "std_dev", "sum", "variance"]

    @staticmethod
    def format(value):
        return float(value) if value is not None else None

    @staticmethod
    def parse(value):
        return float(value)


class TimeFieldType(FieldType):
    default_value = timezone.now().strftime("%Y-%m-%d %H:%M")
    lookups = {
        "equals": "time",
        "not_equals": "time",
        "gt": "time",
        "gte": "time",
        "lt": "time",
        "lte": "time",
        "is_null": "boolean",
    }
    aggregates = ["count"]  # average, min and max might be nice here but sqlite...

    @staticmethod
    def parse(value):
        return timezone.make_aware(dateutil.parser.parse(value))

    @staticmethod
    def format(value):
        return str(timezone.make_naive(value)) if value else None


class HTMLFieldType(FieldType):
    default_value = None
    lookups = {}
    aggregates = []


class BooleanFieldType(FieldType):
    default_value = True
    lookups = {"equals": "boolean", "not_equals": "boolean", "is_null": "boolean"}
    aggregates = ["average", "sum"]

    @staticmethod
    def parse(value):
        value = value.lower()
        if value == "true":
            return True
        elif value == "false":
            return False
        else:
            raise ValueError("Expected 'true' or 'false'")


TYPES = {
    field_type.name: field_type
    for field_type in [
        StringFieldType,
        NumberFieldType,
        TimeFieldType,
        BooleanFieldType,
        HTMLFieldType,
    ]
}


class BoundFieldMixin:
    @property
    def model_path(self):
        return self.orm_bound_field.model_path

    @property
    def model_path_str(self):
        return "__".join(self.model_path)

    @property
    def field_path(self):
        return (self.model_path or []) + [self.name]

    @property
    def field_path_str(self):
        return "__".join(self.field_path)

    @property
    def path(self):
        return self.field_path + ([self.aggregate] if self.aggregate else [])

    @property
    def path_str(self):
        return "__".join(self.path)

    @property
    def name(self):
        return self.orm_bound_field.field.name


@dataclass
class BoundFilter(BoundFieldMixin):
    orm_bound_field: Any
    aggregate: Optional[str]
    pretty_path: Sequence[str]
    lookup: str
    value: str

    @classmethod
    def bind(cls, orm_bound_field, aggregate, pretty_path, query_filter):
        return cls(
            orm_bound_field,
            aggregate,
            pretty_path,
            query_filter.lookup,
            query_filter.value,
        )

    def __post_init__(self):
        self.type_ = self.orm_bound_field.field.type_
        self.parsed = None
        self.err_message = None

        if self.aggregate:
            lookups = NumberFieldType.lookups
        else:
            lookups = self.type_.lookups
        if self.lookup not in lookups:
            self.err_message = f"Bad lookup '{self.lookup}' expected {lookups}"
        else:
            try:
                self.parsed = TYPES[lookups[self.lookup]].parse(self.value)
            except Exception as e:
                self.err_message = str(e) if str(e) else repr(e)

        self.is_valid = not self.err_message


@dataclass
class BoundField(BoundFieldMixin):
    orm_bound_field: Any
    aggregate: Optional[str]
    pretty_path: Sequence[str]
    direction: Optional[str]
    priority: Optional[int]

    def __post_init__(self):
        self.type_ = self.orm_bound_field.field.type_
        self.concrete = self.orm_bound_field.field.concrete

    @classmethod
    def bind(cls, orm_bound_field, aggregate, pretty_path, query_field):
        direction = query_field.direction if orm_bound_field.field.concrete else None
        priority = query_field.priority if orm_bound_field.field.concrete else None
        return cls(orm_bound_field, aggregate, pretty_path, direction, priority)


class BoundQuery:
    def __init__(self, query, orm_models):
        def get_path(parts, model_name):
            from .orm import OrmBoundField  # todo remove this

            orm_bound_field = OrmBoundField()  # todo this should be None
            for part in parts:
                orm_field = orm_models[model_name].fields.get(part)
                if orm_field is None:
                    return None
                orm_bound_field = orm_field.bind(orm_bound_field)
                model_name = orm_field.rel_name
            return orm_bound_field

        def get_orm_field(path):
            orm_bound_field = get_path(path, query.model_name)
            if orm_bound_field and orm_bound_field.field.type_:
                return (
                    orm_bound_field,
                    orm_bound_field.aggregate,
                    orm_bound_field.pretty_path,
                )

            return None, None, None

        self.model_name = query.model_name
        self.orm_models = orm_models

        self.fields = []
        for query_field in query.fields:
            orm_bound_field, aggregate, pretty_path = get_orm_field(query_field.path)
            if orm_bound_field:
                self.fields.append(
                    BoundField.bind(
                        orm_bound_field, aggregate, pretty_path, query_field
                    )
                )

        self.filters = []
        for query_filter in query.filters:
            orm_bound_field, aggregate, pretty_path = get_orm_field(query_filter.path)
            if orm_bound_field:
                self.filters.append(
                    BoundFilter.bind(
                        orm_bound_field, aggregate, pretty_path, query_filter
                    )
                )

    @property
    def sort_fields(self):
        return sorted((f for f in self.fields if f.direction), key=lambda f: f.priority)

    @property
    def calculated_fields(self):
        return {f.path_str for f in self.fields if not f.concrete}

    @property
    def valid_filters(self):
        return [f for f in self.filters if f.is_valid]
