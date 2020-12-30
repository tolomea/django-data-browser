import itertools
import json
from collections import defaultdict

from django.core.serializers.json import DjangoJSONEncoder

from .orm_lookups import get_django_filter
from .query import BoundQuery
from .types import ASC, DSC


def _filter(qs, path_str, filter_):
    negation = False
    lookup = filter_.lookup

    if lookup.startswith("not_"):
        negation = True
        lookup = lookup[4:]

    filter_expression = get_django_filter(
        filter_.orm_bound_field.type_, path_str, lookup, filter_.parsed
    )
    if negation:
        return qs.exclude(filter_expression)
    else:
        return qs.filter(filter_expression)


def _cols_sub_query(bound_query):
    filters = [
        filter_
        for filter_ in bound_query.valid_filters
        if filter_.orm_bound_field.filter_
    ]

    return BoundQuery(
        bound_query.model_name,
        bound_query.col_fields,
        filters,
        bound_query.limit,
        bound_query.orm_model,
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
        bound_query.orm_model,
    )


def get_result_queryset(request, bound_query):
    all_fields = {f.queryset_path_str: f for f in bound_query.bound_fields}
    all_fields.update({f.queryset_path_str: f for f in bound_query.bound_filters})

    qs = bound_query.orm_model.get_queryset(
        request, {f.split("__")[0] for f in all_fields}
    )

    # sql functions and qs annotations
    for field in all_fields.values():
        qs = field.annotate(request, qs)

    # filter normal and sql function fields (aka __date)
    for filter_ in bound_query.valid_filters:
        if filter_.orm_bound_field.filter_:
            qs = _filter(qs, filter_.orm_bound_field.queryset_path_str, filter_)

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
    group_by_fields = [
        field.queryset_path_str for field in bound_query.bound_fields if field.group_by
    ]
    qs = qs.values(*group_by_fields).distinct()

    # aggregates
    aggregate_clauses = dict(
        field.aggregate_clause
        for field in bound_query.bound_fields + bound_query.bound_filters
        if field.aggregate_clause
    )
    qs = qs.annotate(**aggregate_clauses)

    # having, aka filter aggregate fields
    for filter_ in bound_query.valid_filters:
        if filter_.orm_bound_field.having:
            qs = _filter(qs, filter_.orm_bound_field.queryset_path_str, filter_)

    # sort
    sort_fields = []
    for field in bound_query.sort_fields:
        if field.direction is ASC:
            sort_fields.append(field.orm_bound_field.queryset_path_str)
        if field.direction is DSC:
            sort_fields.append(f"-{field.orm_bound_field.queryset_path_str}")
    qs = qs.order_by(*sort_fields)

    return qs[: bound_query.limit]


def _get_result_list(request, bound_query):
    return list(get_result_queryset(request, bound_query))


def _get_objs_for_calculated_fields(request, bound_query, orm_models, res):
    # gather up all the objects to fetch for calculated fields
    to_load = defaultdict(set)
    loading_for = defaultdict(set)
    for field in bound_query.bound_fields:
        if field.model_name:
            loading_for[field.model_name].add(field.name)
            pks = to_load[field.model_name]
            for row in res:
                pks.add(row[field.queryset_path_str])

    # fetch all the calculated field objects
    objs = {}
    for model_name, pks in to_load.items():
        objs[model_name] = (
            orm_models[model_name]
            .get_queryset(request, loading_for[model_name])
            .in_bulk(pks)
        )

    return objs


# dump out the results
def _format_table(fields, data, objs):
    namespace = {"objs": objs, "data": data}

    field_lines = []
    for i, field in enumerate(fields):
        namespace[f"format_{i}"] = field.get_formatter()
        value = f"row[{field.queryset_path_str!r}]"
        if field.model_name:
            value = f"objs[{field.model_name!r}].get({value})"
        field_lines.append(f"{field.path_str!r}: format_{i}({value}),")

    code = ["[None if row is None else {", *field_lines, "} for row in data]"]

    return eval("\n".join(code), namespace)


def _get_fields(row, fields):
    res = []
    for field in fields:
        v = row[field.queryset_path_str]
        if isinstance(v, (list, set)):  # pragma: postgres
            v = tuple(v)
        try:
            hash(v)
        except TypeError:
            v = json.dumps(v, cls=DjangoJSONEncoder)
        res.append((field.queryset_path_str, v))
    return tuple(res)


def _get_data_and_all_keys(bound_query, res):
    data = defaultdict(dict)
    all_row_keys = set()
    all_col_keys = set()
    for row in res:
        row_key = _get_fields(row, bound_query.bound_row_fields)
        col_key = _get_fields(row, bound_query.bound_col_fields)
        data[row_key][col_key] = dict(_get_fields(row, bound_query.bound_data_fields))
        all_row_keys.add(row_key)
        all_col_keys.add(col_key)
    return data, all_row_keys, all_col_keys


def _get_keys(res, fields, all_keys):
    keys = {}  # abuse dict to preserve order while removing duplicates
    if fields:
        for row in res:
            key = _get_fields(row, fields)
            if key in all_keys:
                keys[key] = None
    else:
        if res:
            keys[()] = None
    return keys


def _format_grid(data, col_keys, row_keys, fields, objs):
    body_data = []
    for col_key in col_keys:
        table = []
        for row_key in row_keys:
            table.append(data[row_key].get(col_key, None))
        body_data.append(_format_table(fields, table, objs))
    return body_data


def get_results(request, bound_query, orm_models, with_format_hints):
    if not bound_query.fields:
        return {"rows": [], "cols": [], "body": []}

    res = _get_result_list(request, bound_query)

    if bound_query.bound_col_fields and bound_query.bound_row_fields:
        # need to fetch rows and col titles seperately to get correct sort
        rows_res = _get_result_list(request, _rows_sub_query(bound_query))
        cols_res = _get_result_list(request, _cols_sub_query(bound_query))
    else:
        rows_res = res
        cols_res = res

    objs = _get_objs_for_calculated_fields(request, bound_query, orm_models, res)

    if bound_query.bound_col_fields or bound_query.bound_data_fields:
        data, all_row_keys, all_col_keys = _get_data_and_all_keys(bound_query, res)

        col_keys = _get_keys(cols_res, bound_query.bound_col_fields, all_col_keys)
        row_keys = _get_keys(rows_res, bound_query.bound_row_fields, all_row_keys)

        body_data = _format_grid(
            data, col_keys, row_keys, bound_query.bound_data_fields, objs
        )
        row_data = _format_table(
            bound_query.bound_row_fields, [dict(row) for row in row_keys], objs
        )
        col_data = _format_table(
            bound_query.bound_col_fields, [dict(col) for col in col_keys], objs
        )

        format_hints = {}
        for fields, data in [
            (bound_query.bound_row_fields, row_data),
            (bound_query.bound_col_fields, col_data),
            (
                bound_query.bound_data_fields,
                list(itertools.chain.from_iterable(body_data)),
            ),
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
    else:
        row_data = _format_table(
            bound_query.bound_row_fields,
            [dict(_get_fields(row, bound_query.bound_row_fields)) for row in res],
            objs,
        )

        if with_format_hints:
            format_hints = {
                field.path_str: field.get_format_hints(row_data)
                for field in bound_query.bound_row_fields
            }
        else:
            format_hints = None

        return {
            "rows": row_data,
            "cols": [{}] if res else [],
            "body": [[{}] * len(res)] if res else [],
            "length": len(res),
            "formatHints": format_hints,
        }
