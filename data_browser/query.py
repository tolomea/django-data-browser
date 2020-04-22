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


class Field:
    concrete = True

    def __init__(self, name, query):
        self.name = name
        self.query = query

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.name == other.name
            and self.query == other.query
        )

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', {self.query})"

    def parse(self, lookup, value):
        if lookup == "is_null":
            return parse_boolean(value)
        else:
            return self._parse(value)

    def _parse(self, value):
        return value

    def validate(self, lookup, value):
        if lookup not in self.lookups:
            return f"Bad lookup '{lookup}' expected {self.lookups}"
        try:
            self.parse(lookup, value)
        except Exception as e:
            return str(e) if str(e) else repr(e)
        else:
            return None

    @property
    def default_lookup(self):
        return self.lookups[0]


class StringField(Field):
    lookups = [
        "equals",
        "contains",
        "starts_with",
        "ends_with",
        "regex",
        "not_equals",
        "not_contains",
        "not_starts_with",
        "not_ends_with",
        "not_regex",
        "is_null",
    ]


class NumberField(Field):
    lookups = ["equal", "not_equal", "gt", "gte", "lt", "lte", "is_null"]

    def _parse(self, s):
        return float(s)


class TimeField(Field):
    lookups = ["equal", "not_equal", "gt", "gte", "lt", "lte", "is_null"]

    def _parse(self, s):
        return dateutil.parser.parse(s)


class BooleanField(Field):
    lookups = ["equal", "not_equal", "is_null"]

    def _parse(self, s):
        return parse_boolean(s)


class CalculatedField(Field):
    lookups = []
    concrete = False


class Filter:
    def __init__(self, index, field, lookup, value):
        if not lookup:
            lookup = field.default_lookup

        self.index = index
        self.field = field
        self.lookup = lookup
        self.query = field.query
        self.name = field.name
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
    def __init__(self, query, group):
        # group = fields, groups
        # groups = [name, group]

        self._query = query
        self.app = query.app
        self.model = query.model
        self.base_url = query.base_url

        def bind_fields(group, prefix=""):
            fields, groups = group
            fields = {
                name: field_type(f"{prefix}{name}", query)
                for name, field_type in fields.items()
            }
            groups = {
                name: (f"{prefix}{name}", bind_fields(group, f"{prefix}{name}__"))
                for name, group in groups.items()
            }
            return fields, groups

        self.all_fields_nested = bind_fields(group)

        def flatten_fields(group):
            fields, groups = group
            res = {field.name: field for field in fields.values()}
            for name, (path, group) in groups.items():
                res.update(flatten_fields(group))
            return res

        self.all_fields = flatten_fields(self.all_fields_nested)

    @property
    def sort_fields(self):
        res = []
        for name, direction in self._query.fields.items():
            if name in self.all_fields:
                res.append((self.all_fields[name], direction))
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
                yield Filter(i, field, lookup, value)

    @property
    def fields(self):
        return [f for f in self._query.fields if f in self.all_fields]
