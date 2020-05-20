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
        assert (self.direction is None) == (self.priority is None)


@dataclass
class QueryFilter:
    path: str
    lookup: str
    value: str


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
                    path, priority = field.split("+")
                    fields.append(QueryField(path, ASC, int(priority)))
                elif "-" in field:
                    path, priority = field.split("-")
                    fields.append(QueryField(path, DSC, int(priority)))
                else:
                    fields.append(QueryField(field, None, None))

        filters = []
        for path__lookup, values in dict(get_args).items():
            for value in values:
                path, lookup = path__lookup.rsplit("__", 1)
                filters.append(QueryFilter(path, lookup, value))

        return cls(model_name, fields, filters)

    @property
    def field_str(self):
        field_strs = []
        for field in self.fields:
            direction = {ASC: "+", DSC: "-", None: ""}[field.direction]
            priority = str(field.priority) if field.direction else ""
            field_strs.append(f"{field.path}{direction}{priority}")
        return ",".join(field_strs)

    @property
    def filter_fields(self):
        return [
            (f"{filter.path}__{filter.lookup}", filter.value) for filter in self.filters
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
    aggregates = ["count"]

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
        return "__".join(self.path_parts)

    @property
    def field_path(self):
        if self.model_path:
            return f"{self.model_path}__{self.name}"
        return self.name

    @property
    def path(self):
        if self.aggregate:
            return f"{self.field_path}__{self.aggregate}"
        return self.field_path


@dataclass
class BoundFilter(BoundFieldMixin):
    path_parts: Sequence[str]
    name: str
    aggregate: Optional[str]
    lookup: str
    value: str
    type_: FieldType

    @classmethod
    def bind(cls, path, name, aggregate, query_filter, orm_field):
        return cls(
            path,
            name,
            aggregate,
            query_filter.lookup,
            query_filter.value,
            orm_field.type_,
        )

    def __post_init__(self):
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
    path_parts: Sequence[str]
    name: str
    aggregate: Optional[str]
    direction: Optional[str]
    priority: Optional[int]
    orm_field: Any  # orm.OrmField

    def __post_init__(self):
        self.type_ = self.orm_field.type_
        self.concrete = self.orm_field.concrete

    @classmethod
    def bind(cls, path, name, aggregate, query_field, orm_field):
        direction = query_field.direction if orm_field.concrete else None
        priority = query_field.priority if orm_field.concrete else None
        return cls(path, name, aggregate, direction, priority, orm_field)


class BoundQuery:
    def __init__(self, query, orm_models):
        # orm_models = {model_name: {"fields": {field_name, FieldType}, "fks": {field_name: model_name}}}
        def get_path(parts, model_name):
            for part in parts:
                fk_field = orm_models[model_name].fks.get(part)
                if fk_field is None:
                    return None
                model_name = fk_field.model_name
            return model_name

        def get_orm_field(path):
            parts = path.split("__")

            # path__field
            model_name = get_path(parts[:-1], query.model_name)
            if model_name:
                return (
                    orm_models[model_name].fields.get(parts[-1]),
                    parts[:-1],
                    parts[-1],
                    None,
                )

            # path__aggregate__field
            model_name = get_path(parts[:-2], query.model_name)
            if model_name:
                orm_field = orm_models[model_name].fields.get(parts[-2])
                if orm_field and parts[-1] in orm_field.type_.aggregates:
                    return orm_field, parts[:-2], parts[-2], parts[-1]
            return None, None, None, None

        self.model_name = query.model_name
        self.orm_models = orm_models

        self.fields = []
        for query_field in query.fields:
            orm_field, path, name, aggregate = get_orm_field(query_field.path)
            if orm_field:
                self.fields.append(
                    BoundField.bind(path, name, aggregate, query_field, orm_field)
                )

        self.filters = []
        for query_filter in query.filters:
            orm_field, path, name, aggregate = get_orm_field(query_filter.path)
            if orm_field:
                self.filters.append(
                    BoundFilter.bind(path, name, aggregate, query_filter, orm_field)
                )

    @property
    def sort_fields(self):
        return sorted((f for f in self.fields if f.direction), key=lambda f: f.priority)

    @property
    def calculated_fields(self):
        return {f.path for f in self.fields if not f.concrete}

    @property
    def valid_filters(self):
        return [f for f in self.filters if f.is_valid]
