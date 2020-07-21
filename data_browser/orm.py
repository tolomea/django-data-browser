import logging
from collections import defaultdict

from django.contrib.admin import site
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.forms.models import _get_foreign_key

from .common import settings
from .helpers import AnnotationDescriptor
from .orm_fields import (
    _AGGREGATES,
    _FUNC_MAP,
    _FUNCTIONS,
    _OPEN_IN_ADMIN,
    OrmAdminField,
    OrmAggregateField,
    OrmAnnotatedField,
    OrmCalculatedField,
    OrmConcreteField,
    OrmFkField,
    OrmFunctionField,
    OrmModel,
    get_model_name,
)
from .query import (
    ASC,
    DSC,
    TYPES,
    BooleanType,
    BoundQuery,
    DateTimeType,
    DateType,
    NumberType,
    StringType,
)

_FIELD_MAP = {
    models.BooleanField: BooleanType,
    models.NullBooleanField: BooleanType,
    models.CharField: StringType,
    models.TextField: StringType,
    models.GenericIPAddressField: StringType,
    models.UUIDField: StringType,
    models.DateTimeField: DateTimeType,
    models.DateField: DateType,
    models.DecimalField: NumberType,
    models.FloatField: NumberType,
    models.IntegerField: NumberType,
    models.AutoField: NumberType,
}


def _get_all_admin_fields(request):
    request.data_browser = {"calculated_fields": set(), "fields": set()}

    def from_fieldsets(admin, all_):
        auth_user_compat = settings.DATA_BROWSER_AUTH_USER_COMPAT
        if auth_user_compat and isinstance(admin, UserAdmin):
            obj = admin.model()  # get the change fieldsets, not the add ones
        else:
            obj = None

        for f in flatten_fieldsets(admin.get_fieldsets(request, obj)):
            # skip calculated fields on inlines
            if not isinstance(admin, InlineModelAdmin) or hasattr(admin.model, f):
                yield f

    def visible(model_admin, request):
        if model_admin.has_change_permission(request):
            return True
        if hasattr(model_admin, "has_view_permission"):
            return model_admin.has_view_permission(request)
        else:
            return False  # pragma: no cover  Django < 2.1

    all_admin_fields = defaultdict(set)
    model_admins = {}
    for model, model_admin in site._registry.items():
        model_admins[model] = model_admin
        if visible(model_admin, request):
            all_admin_fields[model].update(from_fieldsets(model_admin, True))
            all_admin_fields[model].update(model_admin.get_list_display(request))
            all_admin_fields[model].add(_OPEN_IN_ADMIN)

            # check the inlines, these are already filtered for access
            for inline in model_admin.get_inline_instances(request):
                try:
                    fk_field = _get_foreign_key(model, inline.model, inline.fk_name)
                except Exception:
                    pass
                else:
                    if inline.model not in model_admins:  # pragma: no branch
                        model_admins[inline.model] = inline
                    all_admin_fields[inline.model].update(from_fieldsets(inline, False))
                    all_admin_fields[inline.model].add(fk_field.name)

    # we always have id and never pk
    for fields in all_admin_fields.values():
        fields.add("id")
        fields.discard("pk")
        fields.discard("__str__")

    return model_admins, all_admin_fields


def _get_calculated_field(request, field_name, model_name, model, admin, model_fields):
    field_func = getattr(admin, field_name, None)
    if isinstance(field_func, AnnotationDescriptor):
        admin_order_field = field_func.admin_order_field
        qs = admin_get_queryset(admin, request, [field_name])

        annotation = qs.query.annotations.get(admin_order_field)
        if not annotation:  # pragma: no cover
            raise Exception(
                f"Can't find annotation '{admin_order_field}' for {admin}.{field_name}"
            )

        field_type = getattr(annotation, "output_field", None)
        if not field_type:  # pragma: no cover
            raise Exception(
                f"Annotation '{admin_order_field}' for {admin}.{field_name} doesn't specify 'output_field'"
            )

        type_ = _get_field_type(model, admin_order_field, field_type)
        if type_:  # pragma: no branch
            return OrmAnnotatedField(
                model_name=model_name,
                name=field_name,
                pretty_name=field_name,
                type_=type_,
                field_type=field_type,
                admin=admin,
                admin_order_field=admin_order_field,
            )
    else:
        return OrmCalculatedField(
            model_name=model_name, name=field_name, pretty_name=field_name, admin=admin
        )


def _get_field_type(model, field_name, field):
    if field.__class__ in _FIELD_MAP:
        return _FIELD_MAP[field.__class__]

    for django_type, field_type in _FIELD_MAP.items():
        if isinstance(field, django_type):
            return field_type

    if settings.DEBUG:  # pragma: no cover
        logging.getLogger(__name__).warning(
            f"DDB {model.__name__}.{field_name} unsupported type {type(field).__name__}"
        )
    return None


def _get_fields_for_model(request, model, admin, admin_fields):
    fields = {}

    model_name = get_model_name(model)
    model_fields = {f.name: f for f in model._meta.get_fields()}

    for field_name in admin_fields[model]:
        field = model_fields.get(field_name)
        if field_name == _OPEN_IN_ADMIN:
            fields[_OPEN_IN_ADMIN] = OrmAdminField(model_name=model_name)
        elif isinstance(field, (ForeignObjectRel, models.ManyToManyField)):
            pass  # TODO 2many support
        elif isinstance(field, models.ForeignKey):
            if field.related_model in admin_fields:
                fields[field_name] = OrmFkField(
                    model_name=model_name,
                    name=field_name,
                    pretty_name=field_name,
                    rel_name=get_model_name(field.related_model),
                )
        elif isinstance(field, type(None)):
            fields[field_name] = _get_calculated_field(
                request, field_name, model_name, model, admin, model_fields
            )
        else:
            field_type = _get_field_type(model, field_name, field)

            if field_type:
                fields[field_name] = OrmConcreteField(
                    model_name=model_name,
                    name=field_name,
                    pretty_name=field_name,
                    type_=field_type,
                )

    return OrmModel(fields=fields, admin=admin)


def _get_fields_for_type(type_):
    aggregates = {
        a: OrmAggregateField(type_.name, a) for a in _AGGREGATES.get(type_, [])
    }
    functions = {
        f: OrmFunctionField(type_.name, f, _FUNC_MAP[f][1])
        for f in _FUNCTIONS.get(type_, [])
    }
    return OrmModel({**aggregates, **functions})


def get_models(request):
    model_admins, admin_fields = _get_all_admin_fields(request)
    models = {
        get_model_name(model): _get_fields_for_model(
            request, model, model_admins[model], admin_fields
        )
        for model in admin_fields
    }
    types = {type_.name: _get_fields_for_type(type_) for type_ in TYPES.values()}

    return {**models, **types}


def _get_django_lookup(field_type, lookup):
    if field_type == StringType and lookup == "equals":
        return "iexact"
    else:
        lookup = {
            "equals": "exact",
            "regex": "iregex",
            "contains": "icontains",
            "starts_with": "istartswith",
            "ends_with": "iendswith",
            "is_null": "isnull",
            "gt": "gt",
            "gte": "gte",
            "lt": "lt",
            "lte": "lte",
        }[lookup]
        return lookup


def _filter(qs, filter_, filter_str):
    negation = False
    lookup = filter_.lookup

    if lookup.startswith("not_"):
        negation = True
        lookup = lookup[4:]

    lookup = _get_django_lookup(filter_.orm_bound_field.type_, lookup)
    filter_str = f"{filter_str}__{lookup}"
    if negation:
        return qs.exclude(**{filter_str: filter_.parsed})
    else:
        return qs.filter(**{filter_str: filter_.parsed})


def _cols_sub_query(bound_query):
    row_fields = [f.unsorted() for f in bound_query.row_fields]
    return BoundQuery(
        bound_query.model_name,
        bound_query.col_fields + row_fields,
        bound_query.valid_filters,
        bound_query.limit,
    )


def _rows_sub_query(bound_query):
    col_fields = [f.unsorted() for f in bound_query.col_fields]
    return BoundQuery(
        bound_query.model_name,
        bound_query.row_fields + col_fields,
        bound_query.valid_filters,
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


def admin_get_queryset(admin, request, fields=()):
    request.data_browser = {"calculated_fields": set(fields), "fields": set(fields)}
    return admin.get_queryset(request)


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
        return tuple(
            (field.queryset_path, row[field.queryset_path]) for field in fields
        )

    col_keys = {}
    for row in cols_res:
        col_keys[get_fields(row, bound_query.bound_col_fields)] = None

    row_keys = {}
    for row in rows_res:
        row_keys[get_fields(row, bound_query.bound_row_fields)] = None

    data = defaultdict(dict)
    for row in res:
        row_key = get_fields(row, bound_query.bound_row_fields)
        col_key = get_fields(row, bound_query.bound_col_fields)
        data[row_key][col_key] = dict(get_fields(row, bound_query.bound_data_fields))

    body = []
    for col_key in col_keys:
        table = []
        for row_key in row_keys:
            table.append(data[row_key].get(col_key, None))
        body.append(format_table(bound_query.bound_data_fields, table))

    return {
        "rows": format_table(
            bound_query.bound_row_fields, [dict(row) for row in row_keys]
        ),
        "cols": format_table(
            bound_query.bound_col_fields, [dict(col) for col in col_keys]
        ),
        "body": body,
        "length": len(res),
    }
