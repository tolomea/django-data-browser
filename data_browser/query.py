import json
import urllib
from collections import defaultdict

import dateutil.parser
from django.urls import reverse

ASC, DSC = "asc", "dsc"


class Query:
    @classmethod
    def from_request(cls, app, model, field_str, media, get_args):
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
        for name__lookup, values in sorted(dict(get_args).items()):
            for value in values:
                name, lookup = name__lookup.rsplit("__", 1)
                filters.append((name, lookup, value))

        res = cls(app, model, fields, media, filters)
        return res

    def __init__(self, app, model, fields, media, filters):
        self.app = app
        self.model = model
        self.fields = fields  # {name: None/ASC/DSC}
        self.media = media
        self.filters = filters  # [(name, lookup, value)]

    @property
    def _data(self):
        return {
            "app": self.app,
            "model": self.model,
            "fields": self.fields,
            "media": self.media,
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
    def base_url(self):
        return reverse(
            "data_browser:query",
            kwargs={
                "app": self.app,
                "model": self.model,
                "fields": self.field_str,
                "media": self.media,
            },
        )

    @property
    def filter_fields(self):
        return [(f"{n}__{l}", v) for (n, l, v) in self.filters]

    @property
    def url(self):
        url = self.base_url
        if self.filters:
            params = urllib.parse.urlencode(
                self.filter_fields, quote_via=urllib.parse.quote_plus, doseq=True
            )
            url = f"{url}?{params}"
        return url

    @property
    def save_params(self):
        filters = defaultdict(list)
        for k, v in self.filter_fields:
            filters[k].append(v)

        return {
            "app": self.app,
            "model": self.model,
            "fields": self.field_str,
            "query": json.dumps(filters),
        }


def parse_boolean(val):
    val = val.lower()
    if val == "true":
        return True
    elif val == "false":
        return False
    else:
        raise ValueError("Expected 'true' or 'false'")


PARSERS = {
    "string": lambda x: x,
    "number": float,
    "time": dateutil.parser.parse,
    "boolean": parse_boolean,
}


class MetaField(type):
    def __repr__(cls):
        return cls.__name__

    @property
    def default_lookup(cls):
        return list(cls.lookups)[0]


class Field(metaclass=MetaField):
    concrete = True

    def __init__(self):
        assert False

    @classmethod
    def parse(cls, lookup, value):
        return PARSERS[cls.lookups[lookup]](value)

    @classmethod
    def validate(cls, lookup, value):
        if lookup not in cls.lookups:
            return f"Bad lookup '{lookup}' expected {cls.lookups}"
        try:
            cls.parse(lookup, value)
        except Exception as e:
            return str(e) if str(e) else repr(e)
        else:
            return None

    @classmethod
    def get_type(cls):
        name = cls.__name__.lower()
        assert name.endswith("field")
        return name[: -len("field")]


class StringField(Field):
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


class NumberField(Field):
    lookups = {
        "equal": "number",
        "not_equal": "number",
        "gt": "number",
        "gte": "number",
        "lt": "number",
        "lte": "number",
        "is_null": "boolean",
    }


class TimeField(Field):
    lookups = {
        "equal": "time",
        "not_equal": "time",
        "gt": "time",
        "gte": "time",
        "lt": "time",
        "lte": "time",
        "is_null": "boolean",
    }


class BooleanField(Field):
    lookups = {"equal": "boolean", "not_equal": "boolean", "is_null": "boolean"}


class CalculatedField(Field):
    lookups = {}
    concrete = False


FIELD_TYPES = [StringField, NumberField, TimeField, BooleanField, CalculatedField]


class Filter:
    def __init__(self, name, index, field, lookup, value):
        if not lookup:
            lookup = field.default_lookup

        self.name = name
        self.index = index
        self.field = field
        self.lookup = lookup
        self.err_message = field.validate(lookup, value)
        self.is_valid = not self.err_message
        self.value = value
        self.parsed = field.parse(lookup, value) if self.is_valid else None

    def __eq__(self, other):
        return (
            self.field == other.field
            and self.lookup == other.lookup
            and self.value == other.value
        )


class BoundQuery:
    def __init__(self, query, root, all_model_fields):
        # all_model_fields = {model: {"fields": {field_name, Field}, "fks": {field_name: model}}}
        self._query = query
        self.app = query.app
        self.model = query.model
        self.base_url = query.base_url

        self.all_model_fields = all_model_fields
        self.root = root

        def _get_field_type(path):
            parts = path.split("__")
            model = root
            for part in parts[:-1]:
                model = all_model_fields[model]["fks"].get(part)
                if model is None:
                    return None
            return all_model_fields[model]["fields"].get(parts[-1])

        def get_nested_fields_for_model(model, all_model_fields, seen=()):
            # res = {field_name: Field}, {field_name: res}
            data = all_model_fields.get(model, {"fields": {}, "fks": {}})

            groups = {}
            for field_name, related_model in data["fks"].items():
                if related_model not in seen:
                    group_fileds = get_nested_fields_for_model(
                        related_model, all_model_fields, seen + (model,)
                    )
                    groups[field_name] = group_fileds
            return data["fields"], groups

        def bind_fields(group, prefix=""):
            fields, groups = group

            res = {f"{prefix}{name}": field_type for name, field_type in fields.items()}

            for name, group in groups.items():
                res.update(bind_fields(group, f"{prefix}{name}__"))

            return res

        group = get_nested_fields_for_model(root, all_model_fields)
        self.all_fields = bind_fields(group)

    @property
    def sort_fields(self):
        res = []
        for name, direction in self._query.fields.items():
            if name in self.all_fields:
                res.append((name, self.all_fields[name], direction))
        return res

    @property
    def calculated_fields(self):
        res = set()
        for name in self._query.fields:
            if name in self.all_fields and not self.all_fields[name].concrete:
                res.add(name)
        return res

    @property
    def filters(self):
        for i, (name, lookup, value) in enumerate(self._query.filters):
            if name in self.all_fields:
                field = self.all_fields[name]
                yield Filter(name, i, field, lookup, value)

    @property
    def fields(self):
        return [f for f in self._query.fields if f in self.all_fields]
