import urllib

import dateutil.parser
from django.urls import reverse
from django.utils import timezone

ASC, DSC = "asc", "dsc"


class Query:
    @classmethod
    def from_request(cls, model_name, field_str, get_args):
        fields = {}
        for field in field_str.split(","):
            if field.strip():
                name = field.lstrip("+-")
                if field.startswith("+"):
                    fields[name] = ASC
                elif field.startswith("-"):
                    fields[name] = DSC
                else:
                    fields[name] = None

        filters = []
        for name__lookup, values in dict(get_args).items():
            for value in values:
                name, lookup = name__lookup.rsplit("__", 1)
                filters.append((name, lookup, value))

        res = cls(model_name, fields, filters)
        return res

    def __init__(self, model_name, fields, filters):
        self.model_name = model_name
        self.fields = fields  # {name: None/ASC/DSC}
        self.filters = filters  # [(name, lookup, value)]

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
        for name, order in self.fields.items():
            field_strs.append(f"{prefix[order]}{name}")
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
    f.name: f
    for f in [
        StringFieldType,
        NumberFieldType,
        TimeFieldType,
        BooleanFieldType,
        HTMLFieldType,
    ]
}


class Filter:
    def __init__(self, path, index, field, lookup, value):
        self.path = path
        self.index = index
        self.field = field
        self.lookup = lookup
        self.value = value

        self.parsed = None
        self.err_message = None

        if lookup not in field.lookups:
            self.err_message = f"Bad lookup '{lookup}' expected {field.lookups}"
        try:
            self.parsed = TYPES[field.lookups[lookup]].parse(value)
        except Exception as e:
            self.err_message = str(e) if str(e) else repr(e)

        self.is_valid = not self.err_message

    def __eq__(self, other):
        return (
            self.field == other.field
            and self.lookup == other.lookup
            and self.value == other.value
        )


class BoundQuery:
    def __init__(self, query, all_model_fields):
        # all_model_fields = {model_name: {"fields": {field_name, FieldType}, "fks": {field_name: model_name}}}
        self._query = query
        self.model_name = query.model_name
        self.all_model_fields = all_model_fields

    def _get_field(self, path):
        parts = path.split("__")
        model_name = self.model_name
        for part in parts[:-1]:
            model_name = self.all_model_fields[model_name]["fks"].get(part)
            if model_name is None:
                return None
        res = self.all_model_fields[model_name]["fields"].get(parts[-1])
        return res

    @property
    def sort_fields(self):
        res = []
        for path, direction in self._query.fields.items():
            field = self._get_field(path)
            if field:
                res.append((path, field["type"], direction))
        return res

    @property
    def calculated_fields(self):
        res = set()
        for path in self._query.fields:
            field = self._get_field(path)
            if field and not field["concrete"]:
                res.add(path)
        return res

    @property
    def filters(self):
        for i, (path, lookup, value) in enumerate(self._query.filters):
            field = self._get_field(path)
            if field:
                yield Filter(path, i, field["type"], lookup, value)

    @property
    def fields(self):
        return {
            path: self._get_field(path)["type"]
            for path in self._query.fields
            if self._get_field(path)
        }
