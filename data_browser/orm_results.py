import itertools
import json
from collections import defaultdict

from .orm_admin import admin_get_queryset
from .orm_fields import _get_django_lookup
from .query import ASC, DSC, BoundQuery


def _filter(qs, filter_, filter_str):
    negation = False
    lookup = filter_.lookup

    if lookup.startswith("not_"):
        negation = True
        lookup = lookup[4:]

    filter_value = filter_.parsed
    lookup, filter_value = _get_django_lookup(
        filter_.orm_bound_field.type_, lookup, filter_value
    )
    filter_str = f"{filter_str}__{lookup}"
    if lookup == "contains":  # pragma: postgres
        filter_value = [filter_value]
    if negation:
        return qs.exclude(**{filter_str: filter_value})
    else:
        return qs.filter(**{filter_str: filter_value})


def _cols_sub_query(bound_query):
    filters = [
        filter_
        for filter_ in bound_query.valid_filters
        if filter_.orm_bound_field.filter_
    ]

    return BoundQuery(
        bound_query.model_name, bound_query.col_fields, filters, bound_query.limit
    )


def _rows_sub_query(bound_query):
    filters = [
        filter_
        for filter_ in bound_query.valid_filters
        if filter_.orm_bound_field.filter_
    ]
    data_fields = [f for f in bound_query.data_fields if f.direction]
    return BoundQuery(
        bound_query.model_name,
        bound_query.row_fields + data_fields,
        filters,
        bound_query.limit,
    )


def _get_results(request, bound_query, orm_models):
    all_fields = {f.queryset_path: f for f in bound_query.bound_fields}
    all_fields.update({f.queryset_path: f for f in bound_query.bound_filters})

    admin = orm_models[bound_query.model_name].admin
    qs = admin_get_queryset(admin, request, {f.split("__")[0] for f in all_fields})

    # sql functions and qs annotations
    for field in all_fields.values():
        qs = field.annotate(request, qs)

    # filter normal and sql function fields (aka __date)
    for filter_ in bound_query.valid_filters:
        if filter_.orm_bound_field.filter_:
            qs = _filter(qs, filter_, filter_.orm_bound_field.queryset_path)

    # nothing to group on, early out with an aggregate
    if not any(f.group_by for f in bound_query.bound_fields):
        return [
            qs.aggregate(
                **dict(
                    field.aggregate_clause
                    for field in bound_query.bound_fields + bound_query.bound_filters
                    if field.aggregate_clause
                )
            )
        ]

    # group by
    qs = qs.values(
        *[field.queryset_path for field in bound_query.bound_fields if field.group_by]
    ).distinct()

    # aggregates
    qs = qs.annotate(
        **dict(
            field.aggregate_clause
            for field in bound_query.bound_fields + bound_query.bound_filters
            if field.aggregate_clause
        )
    )

    # having, aka filter aggregate fields
    for filter_ in bound_query.valid_filters:
        if filter_.orm_bound_field.having:
            qs = _filter(qs, filter_, filter_.orm_bound_field.queryset_path)

    # sort
    sort_fields = []
    for field in bound_query.sort_fields:
        if field.direction is ASC:
            sort_fields.append(field.orm_bound_field.queryset_path)
        if field.direction is DSC:
            sort_fields.append(f"-{field.orm_bound_field.queryset_path}")
    qs = qs.order_by(*sort_fields)

    return list(qs[: bound_query.limit])


def get_results(request, bound_query, orm_models):
    if not bound_query.fields:
        return {"rows": [], "cols": [], "body": []}

    if bound_query.bound_col_fields and bound_query.bound_row_fields:
        res = _get_results(request, bound_query, orm_models)
        rows_res = _get_results(request, _rows_sub_query(bound_query), orm_models)
        cols_res = _get_results(request, _cols_sub_query(bound_query), orm_models)
    else:
        res = _get_results(request, bound_query, orm_models)
        rows_res = res
        cols_res = res

    # gather up all the objects to fetch for calculated fields
    to_load = defaultdict(set)
    loading_for = defaultdict(set)
    for field in bound_query.bound_fields:
        if field.model_name:
            loading_for[field.model_name].add(field.name)
            pks = to_load[field.model_name]
            for row in res:
                pks.add(row[field.queryset_path])

    # fetch all the calculated field objects
    cache = {}
    for model_name, pks in to_load.items():
        admin = orm_models[model_name].admin
        cache[model_name] = admin_get_queryset(
            admin, request, loading_for[model_name]
        ).in_bulk(pks)

    # dump out the results
    def format_table(fields, data):
        results = []
        for row in data:
            if row:
                res_row = {}
                for field in fields:
                    value = row[field.queryset_path]
                    if field.model_name:
                        value = cache[field.model_name].get(value)
                    res_row[field.path_str] = field.format(value)
                results.append(res_row)
            else:
                results.append(row)
        return results

    def get_fields(row, fields):
        res = []
        for field in fields:
            v = row[field.queryset_path]
            if isinstance(v, list):  # pragma: postgres
                v = tuple(v)
            try:
                hash(v)
            except TypeError:
                v = json.dumps(v)
            res.append((field.queryset_path, v))
        return tuple(res)

    data = defaultdict(dict)
    all_row_keys = set()
    all_col_keys = set()
    for row in res:
        row_key = get_fields(row, bound_query.bound_row_fields)
        col_key = get_fields(row, bound_query.bound_col_fields)
        data[row_key][col_key] = dict(get_fields(row, bound_query.bound_data_fields))
        all_row_keys.add(row_key)
        all_col_keys.add(col_key)

    col_keys = {}  # abuse dict to preserve order while removing duplicates
    for row in cols_res:
        key = get_fields(row, bound_query.bound_col_fields)
        if key in all_col_keys:
            col_keys[key] = None

    row_keys = {}  # abuse dict to preserve order while removing duplicates
    for row in rows_res:
        key = get_fields(row, bound_query.bound_row_fields)
        if key in all_row_keys:
            row_keys[key] = None

    body_data = []
    for col_key in col_keys:
        table = []
        for row_key in row_keys:
            table.append(data[row_key].get(col_key, None))
        body_data.append(format_table(bound_query.bound_data_fields, table))

    row_data = format_table(
        bound_query.bound_row_fields, [dict(row) for row in row_keys]
    )
    col_data = format_table(
        bound_query.bound_col_fields, [dict(col) for col in col_keys]
    )

    format_hints = {}
    for fields, data in [
        (bound_query.bound_row_fields, row_data),
        (bound_query.bound_col_fields, col_data),
        (bound_query.bound_data_fields, itertools.chain.from_iterable(body_data)),
    ]:
        format_hints.update(
            {field.path_str: field.get_format_hints(data) for field in fields}
        )

    return {
        "rows": row_data,
        "cols": col_data,
        "body": body_data,
        "length": len(res),
        "formatHints": format_hints,
    }
