import urllib
from dataclasses import dataclass
from typing import Optional, Sequence

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

        res = cls(model_name, fields, filters)
        return res

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
    default_value = ""

    def __init__(self):
        assert False

    @staticmethod
    def format(value):
        return value

    @staticmethod
    def parse(value):
        return value


class StringFieldType(FieldType):
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

    @staticmethod
    def parse(value):
        return float(value)


class TimeFieldType(FieldType):
    lookups = {
        "equals": "time",
        "not_equals": "time",
        "gt": "time",
        "gte": "time",
        "lt": "time",
        "lte": "time",
        "is_null": "boolean",
    }
    default_value = timezone.now().strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def parse(value):
        return timezone.make_aware(dateutil.parser.parse(value))

    @staticmethod
    def format(value):
        return timezone.make_naive(value) if value else None


class HTMLFieldType(FieldType):
    lookups = {}


class BooleanFieldType(FieldType):
    default_value = True
    lookups = {"equals": "boolean", "not_equals": "boolean", "is_null": "boolean"}

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


@dataclass
class BoundFilter:
    path: str
    lookup: str
    value: str
    type_: FieldType

    @classmethod
    def bind(cls, query_filter, orm_field):
        return cls(
            query_filter.path, query_filter.lookup, query_filter.value, orm_field.type_
        )

    def __post_init__(self):
        self.parsed = None
        self.err_message = None

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
class BoundField:
    path: str
    direction: Optional[str]
    priority: Optional[int]
    concrete: bool
    type_: FieldType

    @classmethod
    def bind(cls, query_field, orm_field):
        direction = query_field.direction if orm_field.concrete else None
        priority = query_field.priority if orm_field.concrete else None
        return cls(
            query_field.path, direction, priority, orm_field.concrete, orm_field.type_
        )


class BoundQuery:
    def __init__(self, query, orm_models):
        # orm_models = {model_name: {"fields": {field_name, FieldType}, "fks": {field_name: model_name}}}
        def get_orm_field(path):
            parts = path.split("__")
            model_name = query.model_name
            for part in parts[:-1]:
                fk_field = orm_models[model_name].fks.get(part)
                if fk_field is None:
                    return None
                model_name = fk_field.model_name
            res = orm_models[model_name].fields.get(parts[-1])
            return res

        self.model_name = query.model_name
        self.orm_models = orm_models

        self.fields = []
        for query_field in query.fields:
            orm_field = get_orm_field(query_field.path)
            if orm_field:
                self.fields.append(BoundField.bind(query_field, orm_field))

        self.filters = []
        for query_filter in query.filters:
            orm_field = get_orm_field(query_filter.path)
            if orm_field:
                self.filters.append(BoundFilter.bind(query_filter, orm_field))

    @property
    def sort_fields(self):
        return sorted((f for f in self.fields if f.direction), key=lambda f: f.priority)

    @property
    def calculated_fields(self):
        return {f.path for f in self.fields if not f.concrete}
