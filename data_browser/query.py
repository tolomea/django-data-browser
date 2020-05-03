import urllib
from dataclasses import dataclass
from typing import Optional

import dateutil.parser
from django.urls import reverse
from django.utils import timezone

ASC, DSC = "asc", "dsc"


@dataclass
class QueryField:
    path: str
    direction: Optional[str]


class Query:
    @classmethod
    def from_request(cls, model_name, field_str, get_args):
        fields = []
        for field in field_str.split(","):
            if field.strip():
                path = field.lstrip("+-")
                if field.startswith("+"):
                    fields.append(QueryField(path, ASC))
                elif field.startswith("-"):
                    fields.append(QueryField(path, DSC))
                else:
                    fields.append(QueryField(path, None))

        filters = []
        for path__lookup, values in dict(get_args).items():
            for value in values:
                path, lookup = path__lookup.rsplit("__", 1)
                filters.append((path, lookup, value))

        res = cls(model_name, fields, filters)
        return res

    def __init__(self, model_name, fields, filters):
        self.model_name = model_name
        self.fields = fields
        self.filters = filters

    @property
    def _data(self):
        return {
            "model_name": self.model_name,
            "fields": self.fields,
            "filters": self.filters,
        }

    def __eq__(self, other):
        return self._data == other._data

    @property
    def field_str(self):
        prefix = {ASC: "+", DSC: "-", None: ""}
        field_strs = []
        for field in self.fields:
            field_strs.append(f"{prefix[field.direction]}{field.path}")
        return ",".join(field_strs)

    @property
    def filter_fields(self):
        return [(f"{n}__{l}", v) for (n, l, v) in self.filters]

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
        return timezone.make_naive(value)


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


class BoundFilter:
    def __init__(self, path, index, type_, lookup, value):
        self.path = path
        self.index = index
        self.type_ = type_
        self.lookup = lookup
        self.value = value

        self.parsed = None
        self.err_message = None

        if lookup not in type_.lookups:
            self.err_message = f"Bad lookup '{lookup}' expected {type_.lookups}"
        else:
            try:
                self.parsed = TYPES[type_.lookups[lookup]].parse(value)
            except Exception as e:
                self.err_message = str(e) if str(e) else repr(e)

        self.is_valid = not self.err_message

    def __eq__(self, other):
        return (
            self.type_ == other.type_
            and self.lookup == other.lookup
            and self.value == other.value
        )


class BoundField:
    def __init__(self, query_field, orm_field):
        self.path = query_field.path
        self.concrete = orm_field.concrete
        self.type_ = orm_field.type_
        self.direction = query_field.direction if self.concrete else None


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
                self.fields.append(BoundField(query_field, orm_field))

        self.filters = []
        for i, (path, lookup, value) in enumerate(query.filters):
            orm_field = get_orm_field(path)
            if orm_field:
                self.filters.append(
                    BoundFilter(path, i, orm_field.type_, lookup, value)
                )

    @property
    def sort_fields(self):
        return [f for f in self.fields if f.direction]

    @property
    def calculated_fields(self):
        return {f.path for f in self.fields if not f.concrete}
