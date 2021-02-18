import cProfile
import csv
import io
import itertools
import json
import marshal
import pstats
import sys

import django.contrib.admin.views.decorators as admin_decorators
import hyperlink
import sqlparse
from django import http
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404
from django.template import engines, loader
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators import csrf

from . import version
from .common import HttpResponse, JsonResponse, can_make_public, settings
from .models import View
from .orm_admin import OPEN_IN_ADMIN, get_models
from .orm_results import get_result_queryset, get_results
from .query import BoundQuery, Query, QueryFilter
from .types import TYPES


def _get_query_data(bound_query):
    return {
        "filters": [
            {
                "pathStr": filter_.path_str,
                "lookup": filter_.lookup,
                "value": filter_.value,
            }
            for filter_ in bound_query.filters
        ],
        "filterErrors": [filter_.err_message for filter_ in bound_query.filters],
        "parsedFilterValues": [
            filter_.formatted_value() for filter_ in bound_query.filters
        ],
        "fields": [
            {
                "pathStr": field.path_str,
                "sort": field.direction,
                "priority": field.priority,
                "pivoted": field.pivoted,
            }
            for field in bound_query.fields
        ],
        "model": bound_query.model_name,
        "limit": bound_query.limit,
    }


def _get_model_fields(model_name, orm_models):
    orm_model = orm_models[model_name]

    def sort_model_fields(fields):
        front = {orm_model.pk: 1, OPEN_IN_ADMIN: 2}
        sorted_fields = sorted(
            fields.items(),
            key=lambda name_field: (
                front.get(name_field[0], sys.maxsize),
                name_field[1]["prettyName"],
            ),
        )
        return [name for name, field in sorted_fields]

    all_fields = {
        name: {
            "model": orm_field.rel_name,
            "type": orm_field.type_.name if orm_field.type_ else None,
            "concrete": orm_field.concrete,
            "canPivot": orm_field.can_pivot,
            "prettyName": orm_field.pretty_name,
            "choices": [v for k, v in orm_field.choices],
            "defaultSort": orm_field.default_sort,
            "actions": [
                {"name": name, "prettyName": desc}
                for name, (func, desc) in sorted((orm_field.actions or {}).items())
            ],
        }
        for name, orm_field in orm_model.fields.items()
    }

    q = Query(model_name, [], [QueryFilter(*f) for f in orm_model.default_filters])
    bq = BoundQuery.bind(q, orm_models)

    return {
        "fields": all_fields,
        "sortedFields": sort_model_fields(all_fields),
        "defaultFilters": [
            {
                "pathStr": filter_.path_str,
                "lookup": filter_.lookup,
                "value": filter_.value,
            }
            for filter_ in bq.filters
        ],
    }


def _get_config(request):
    orm_models = get_models(request)
    types = {
        name: {
            "lookups": {
                n: {"prettyName": tn, "type": t} for n, (tn, t) in type_.lookups.items()
            },
            "sortedLookups": list(type_.lookups),
            "defaultLookup": type_.default_lookup,
            "defaultValue": type_.default_value,
        }
        for name, type_ in TYPES.items()
    }

    all_model_fields = {
        model_name: _get_model_fields(model_name, orm_models)
        for model_name in orm_models
    }

    return {
        "baseUrl": reverse("data_browser:home"),
        "types": types,
        "allModelFields": all_model_fields,
        "sortedModels": sorted(
            name for name, model in orm_models.items() if model.root
        ),
        "canMakePublic": can_make_public(request.user),
        "sentryDsn": settings.DATA_BROWSER_FE_DSN,
        "defaultRowLimit": settings.DATA_BROWSER_DEFAULT_ROW_LIMIT,
    }


@admin_decorators.staff_member_required
def query_ctx(request, *, model_name="", fields=""):
    config = _get_config(request)
    return JsonResponse(config)


def admin_action(request, model_name, fields):
    data = json.loads(request.body)
    action = data["action"]
    field = data["field"]

    if field not in fields:
        raise http.Http404(f"bad field '{field}'")  # pragma: no cover

    params = hyperlink.parse(request.get_full_path()).query
    query = Query.from_request(model_name, field, params)

    orm_models = get_models(request)
    if query.model_name not in orm_models:
        raise http.Http404(f"'{query.model_name}' does not exist")  # pragma: no cover

    bound_query = BoundQuery.bind(query, orm_models)

    results = get_results(request, bound_query, orm_models, False)

    pks = {row.get(field) for row in results["rows"]} | {
        col.get(field) for col in results["cols"]
    }
    pks -= {None}

    model_name = bound_query.fields[0].orm_bound_field.field.model_name
    return orm_models[model_name].get_action_request(request, action, pks)


@csrf.csrf_protect
@csrf.ensure_csrf_cookie
@admin_decorators.staff_member_required
def query_html(request, *, model_name="", fields=""):
    if request.method == "POST":
        return admin_action(request, model_name, fields)

    config = _get_config(request)
    config = json.dumps(config, cls=DjangoJSONEncoder)
    config = (
        config.replace("<", "\\u003C").replace(">", "\\u003E").replace("&", "\\u0026")
    )

    if settings.DATA_BROWSER_DEV:  # pragma: no cover
        try:
            response = _get_from_js_dev_server(request, "get")
        except Exception as e:
            return HttpResponse(f"Error loading from JS dev server.<br><br>{e}")

        template = engines["django"].from_string(response.text)
    else:
        template = loader.get_template("data_browser/index.html")

    return TemplateResponse(request, template, {"config": config, "version": version})


@admin_decorators.staff_member_required
def query(request, *, model_name, fields="", media):
    params = hyperlink.parse(request.get_full_path()).query

    if media.startswith("profile") or media.startswith("pstats"):
        if "_" in media:
            prof_media, media = media.split("_")
        else:
            prof_media = media
            media = "json"

        profiler = cProfile.Profile()
        try:
            profiler.enable()

            query = Query.from_request(model_name, fields, params)
            for x in _data_response(request, query, media, privileged=True):
                pass

            profiler.disable()

            if prof_media == "profile":
                buffer = io.StringIO()
                stats = pstats.Stats(profiler, stream=buffer)
                stats.sort_stats("cumulative").print_stats(50)
                stats.sort_stats("time").print_stats(50)
                buffer.seek(0)
                return HttpResponse(buffer, content_type="text/plain")
            elif prof_media == "pstats":
                buffer = io.BytesIO()
                marshal.dump(pstats.Stats(profiler).stats, buffer)
                buffer.seek(0)
                response = HttpResponse(buffer, content_type="application/octet-stream")
                response[
                    "Content-Disposition"
                ] = f"attachment; filename={query.model_name}-{timezone.now().isoformat()}.pstats"
                return response
            else:
                raise http.Http404(f"Bad file format {prof_media} requested")
        finally:
            if profiler:  # pragma: no branch
                profiler.disable()
    else:
        query = Query.from_request(model_name, fields, params)
        return _data_response(request, query, media, privileged=True)


def view(request, pk, media):
    view = get_object_or_404(View.objects.filter(public=True), public_slug=pk)
    if (
        # some of these are checked by the admin but this is a good time to be paranoid
        view.owner.is_active
        and view.owner.is_staff
        and can_make_public(view.owner)
        and settings.DATA_BROWSER_ALLOW_PUBLIC
    ):
        request.user = view.owner  # public views are run as the person who owns them
        query = view.get_query()
        return _data_response(request, query, media, privileged=False, strict=True)
    else:
        raise http.Http404("No View matches the given query.")


def pad(x):
    return [None] * max(0, x)


def concat(*lists):
    return itertools.chain.from_iterable(lists)


def flip_table(table):
    return (list(x) for x in zip(*table))


def join_tables(*tables):
    return (list(concat(*ts)) for ts in zip(*tables))


def format_table(fields, table, spacing=0):
    return concat(
        [[" ".join(f.pretty_path) for f in fields]],
        *[
            [[(row[f.path_str] if row else "") for f in fields]]
            + [pad(len(fields))] * spacing
            for row in table
        ],
    )


def pad_table(x, table):
    p = pad(x)
    return (p + row for row in table)


class Echo:
    def write(self, value):
        return value


def _data_response(request, query, media, privileged=False, strict=False):
    orm_models = get_models(request)
    if query.model_name not in orm_models:
        raise http.Http404(f"{query.model_name} does not exist")
    bound_query = BoundQuery.bind(query, orm_models)

    if strict and not all(f.is_valid for f in bound_query.filters):
        return http.HttpResponseBadRequest()

    if media == "csv":
        results = get_results(request, bound_query, orm_models, False)

        def csv_rows():
            # the pivoted column headers
            yield from pad_table(
                len(bound_query.row_fields) - 1,
                flip_table(
                    format_table(
                        bound_query.col_fields,
                        results["cols"],
                        spacing=len(bound_query.data_fields) - 1,
                    )
                ),
            )

            # the row headers and data area
            yield from pad_table(
                1 - len(bound_query.row_fields),
                join_tables(
                    format_table(bound_query.row_fields, results["rows"]),
                    *(
                        format_table(bound_query.data_fields, sub_table)
                        for sub_table in results["body"]
                    ),
                ),
            )

        writer = csv.writer(Echo())
        response = http.StreamingHttpResponse(
            (writer.writerow(row) for row in csv_rows()), content_type="text/csv"
        )
        response[
            "Content-Disposition"
        ] = f"attachment; filename={query.model_name}-{timezone.now().isoformat()}.csv"
        return response
    elif media == "json":
        results = get_results(request, bound_query, orm_models, True)
        resp = _get_query_data(bound_query) if privileged else {}
        resp.update(results)
        return JsonResponse(resp)
    elif privileged and media == "query":
        resp = _get_query_data(bound_query)
        return JsonResponse(resp)
    elif privileged and media in ["sql", "explain"]:
        query_set = get_result_queryset(request, bound_query)
        if isinstance(query_set, list):
            res = "Not available for pure aggregates"
        else:
            if media == "sql":
                res = sqlparse.format(
                    str(query_set.query), reindent=True, keyword_case="upper"
                )
            elif media == "explain":
                res = query_set.explain()
            else:
                assert False
        return HttpResponse(res, content_type="text/plain")
    else:
        raise http.Http404(f"Bad file format {media} requested")


def _get_from_js_dev_server(request, method=None):  # pragma: no cover
    import requests

    if method is None:
        method = request.META["REQUEST_METHOD"].lower()

    upstream_url = f"http://127.0.0.1:3000{request.path}"
    sys.stdout.write(f"Proxy request: {method} {upstream_url}\n")
    return getattr(requests, method)(upstream_url, stream=True)


@csrf.csrf_exempt
def proxy_js_dev_server(request, path):  # pragma: no cover
    """
    Proxy HTTP requests to the frontend dev server in development.

    The implementation is very basic e.g. it doesn't handle HTTP headers.

    """
    response = _get_from_js_dev_server(request)
    return http.StreamingHttpResponse(
        streaming_content=response.iter_content(2 ** 12),
        content_type=response.headers.get("Content-Type"),
        status=response.status_code,
        reason=response.reason,
    )
