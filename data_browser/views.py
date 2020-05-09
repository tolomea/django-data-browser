import csv
import io
import json
import sys

import django.contrib.admin.views.decorators as admin_decorators
from django import http
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template import engines, loader
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import View
from .orm import _OPEN_IN_ADMIN, get_data, get_models
from .query import TYPES, BoundQuery, Query


def _get_query_data(bound_query):
    return {
        "filters": [
            {
                "errorMessage": filter_.err_message,
                "path": filter_.path,
                "lookup": filter_.lookup,
                "value": filter_.value,
            }
            for filter_ in bound_query.filters
        ],
        "fields": [
            {"path": field.path, "sort": field.direction, "priority": field.priority}
            for field in bound_query.fields
        ],
        "model": bound_query.model_name,
    }


def _get_config(orm_models):
    types = {
        name: {
            "lookups": {n: {"type": t} for n, t in type_.lookups.items()},
            "sortedLookups": list(type_.lookups),
            "defaultLookup": type_.default_lookup,
            "defaultValue": type_.default_value,
        }
        for name, type_ in TYPES.items()
    }

    def sort_model_fields(fields):
        fields = sorted(fields)
        front = {"id": 1, _OPEN_IN_ADMIN: 2}
        return sorted(fields, key=lambda x: front.get(x, sys.maxsize))

    orm_models = {
        model_name: {
            "fields": {
                name: {"type": orm_field.type_.name, "concrete": orm_field.concrete}
                for name, orm_field in orm_model.fields.items()
            },
            "fks": {
                name: {"model": fk_field.model_name}
                for name, fk_field in orm_model.fks.items()
            },
            "sorted_fields": sort_model_fields(orm_model.fields),
            "sorted_fks": sorted(orm_model.fks),
        }
        for model_name, orm_model in orm_models.items()
    }

    return {
        "baseUrl": reverse("data_browser:home"),
        "adminUrl": reverse(f"admin:{View._meta.db_table}_add"),
        "types": types,
        "allModelFields": orm_models,
        "sortedModels": sorted(orm_models),
    }


def _get_context(request, model_name, fields):
    query = Query.from_request(model_name, fields, request.GET)
    orm_models = get_models(request)
    if query.model_name and query.model_name not in orm_models:
        raise http.Http404(f"query.model_name does not exist")
    bound_query = BoundQuery(query, orm_models)
    return {
        "config": _get_config(orm_models),
        "initialState": {"data": [], **_get_query_data(bound_query)},
        "sentryDsn": getattr(settings, "DATA_BROWSER_FE_DSN", None),
    }


@admin_decorators.staff_member_required
def query_ctx(request, *, model_name, fields=""):  # pragma: no cover
    ctx = _get_context(request, model_name, fields)
    return JsonResponse(ctx)


@admin_decorators.staff_member_required
def query_html(request, *, model_name="", fields=""):
    ctx = _get_context(request, model_name, fields)
    ctx = json.dumps(ctx)
    ctx = ctx.replace("<", "\\u003C").replace(">", "\\u003E").replace("&", "\\u0026")

    if getattr(settings, "DATA_BROWSER_DEV", False):  # pragma: no cover
        response = _get_from_js_dev_server(request)
        template = engines["django"].from_string(response.text)
    else:
        template = loader.get_template("data_browser/index.html")

    return TemplateResponse(request, template, {"ctx": ctx})


@admin_decorators.staff_member_required
def query(request, *, model_name, fields="", media):
    query = Query.from_request(model_name, fields, request.GET)
    return _data_response(request, query, media)


def view(request, pk, media):
    view = get_object_or_404(View.objects.filter(public=True), pk=pk)
    request.user = view.owner  # public views are run as the person who owns them
    query = view.get_query()
    return _data_response(request, query, media)


def _data_response(request, query, media):
    orm_models = get_models(request)
    if query.model_name not in orm_models:
        raise http.Http404(f"query.model_name does not exist")
    bound_query = BoundQuery(query, orm_models)
    data = get_data(request, bound_query)

    if media == "csv":
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(f.path for f in bound_query.fields)
        writer.writerows(data)
        buffer.seek(0)
        response = HttpResponse(buffer, content_type="text/csv")
        response[
            "Content-Disposition"
        ] = f"attachment; filename={query.model_name}-{timezone.now().isoformat()}.csv"
        return response
    elif media == "json":
        resp = _get_query_data(bound_query)
        resp["data"] = data
        return JsonResponse(resp)
    else:
        assert False


def _get_from_js_dev_server(request):  # pragma: no cover
    import requests

    upstream_url = f"http://localhost:3000{request.path}"
    method = request.META["REQUEST_METHOD"].lower()
    return getattr(requests, method)(upstream_url, stream=True)


@csrf_exempt
def proxy_js_dev_server(request, path):  # pragma: no cover
    """
    Proxy HTTP requests to the frontend dev server in development.

    The implementation is very basic e.g. it doesn't handle HTTP headers.

    """
    response = _get_from_js_dev_server(request)
    content_type = response.headers.get("Content-Type")

    if request.META.get("HTTP_UPGRADE", "").lower() == "websocket":
        return http.HttpResponse(
            content="WebSocket connections aren't supported",
            status=501,
            reason="Not Implemented",
        )

    else:
        return http.StreamingHttpResponse(
            streaming_content=response.iter_content(2 ** 12),
            content_type=content_type,
            status=response.status_code,
            reason=response.reason,
        )
