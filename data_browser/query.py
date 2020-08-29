import urllib
from dataclasses import dataclass
from typing import Any, Optional, Sequence

from django.urls import reverse

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
                    try:
                        limit = max(1, int(value))
                    except:  # noqa: E722  input sanitization
                        pass
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
                if model_name is None:
                    return None
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
