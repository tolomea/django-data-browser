import csv
import io
import json

import django.contrib.admin.views.decorators as admin_decorators
import requests
from django import http
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template import engines, loader
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .db import get_all_model_fields, get_data
from .models import View
from .query import TYPES, BoundQuery, Query


def _get_query_data(bound_query):
    return {
        "filters": [
            {
                "errorMessage": filter_.err_message,
                "name": filter_.name,
                "lookup": filter_.lookup,
                "value": filter_.value,
            }
            for filter_ in bound_query.filters
        ],
        "fields": [
            {"name": name, "sort": sort_direction}
            for (name, field, sort_direction) in bound_query.sort_fields
        ],
        "model": bound_query.model_name,
    }


def _get_config(all_model_fields):
    types = {
        name: {
            "lookups": {n: {"type": t} for n, t in type_.lookups.items()},
            "sortedLookups": list(type_.lookups),
            "defaultLookup": type_.default_lookup,
            "defaultValue": type_.default_value,
        }
        for name, type_ in TYPES.items()
    }

    front_fields = ["pk", "admin"]
    all_model_fields = {
        model_name: {
            "fields": {
                name: {"type": field["type"].name, "concrete": field["concrete"]}
                for name, field in model_fields["fields"].items()
            },
            "fks": {
                name: {"model": rel_model}
                for name, rel_model in model_fields["fks"].items()
            },
            "sorted_fields": front_fields
            + sorted(f for f in model_fields["fields"] if f not in front_fields),
            "sorted_fks": sorted(model_fields["fks"]),
        }
        for model_name, model_fields in all_model_fields.items()
    }

    return {
        "baseUrl": reverse("data_browser:root"),
        "adminUrl": reverse(f"admin:{View._meta.db_table}_add"),
        "types": types,
        "allModelFields": all_model_fields,
        "sortedModels": sorted(all_model_fields),
    }


def _get_context(request, model_name, fields):
    query = Query.from_request(model_name, fields, request.GET)
    all_model_fields = get_all_model_fields(request)
    if query.model_name not in all_model_fields:
        raise http.Http404(f"query.model_name does not exist")
    bound_query = BoundQuery(query, all_model_fields)
    return {**_get_config(all_model_fields), **_get_query_data(bound_query)}


@admin_decorators.staff_member_required
def query_ctx(request, *, model_name, fields=""):  # pragma: no cover
    ctx = _get_context(request, model_name, fields)
    return JsonResponse(ctx)


@admin_decorators.staff_member_required
def query_html(request, *, model_name, fields=""):
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
    all_model_fields = get_all_model_fields(request)
    if query.model_name not in all_model_fields:
        raise http.Http404(f"query.model_name does not exist")
    bound_query = BoundQuery(query, all_model_fields)
    data = get_data(bound_query)

    if media == "csv":
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(bound_query.fields)
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
