import json
from collections import defaultdict

import django.contrib.admin.views.decorators as admin_decorators
from django.shortcuts import get_object_or_404
from django.views.decorators import csrf

from .common import HttpResponse, JsonResponse, can_make_public
from .models import View, global_data


def clean_str(field, value):
    return value[: View._meta.get_field(field).max_length]


def clean_uint(field, value):
    try:
        value = int(value)
    except Exception:  # noqa: E722  input sanitization
        value = 1
    return max(value, 1)


def clean_noop(field, value):
    return value


WRITABLE_FIELDS = [  # model_field_name, api_field_name, clean
    ("name", "name", clean_str),
    ("description", "description", clean_noop),
    ("public", "public", clean_noop),
    ("model_name", "model", clean_noop),
    ("fields", "fields", clean_noop),
    ("query", "query", clean_noop),
    ("limit", "limit", clean_uint),
    ("folder", "folder", clean_str),
]


def deserialize(request):
    data = json.loads(request.body)

    res = {
        model_field_name: clean(model_field_name, data[api_field_name])
        for model_field_name, api_field_name, clean in WRITABLE_FIELDS
        if api_field_name in data
    }

    # perm check
    if not can_make_public(request.user):
        res["public"] = False

    return res


def serialize(view):
    return {
        **{
            api_field_name: getattr(view, model_field_name)
            for model_field_name, api_field_name, clean in WRITABLE_FIELDS
        },
        "publicLink": view.public_link(),
        "googleSheetsFormula": view.google_sheets_formula(),
        "link": view.get_query().get_url("html"),
        "createdTime": f"{view.created_time:%Y-%m-%d %H:%M:%S}",
        "pk": view.pk,
    }


def get_queryset(request):
    return View.objects.filter(owner=request.user)


@csrf.csrf_protect
@admin_decorators.staff_member_required
def view_list(request):
    global_data.request = request

    if request.method == "GET":
        grouped_views = defaultdict(list)
        for view in get_queryset(request).order_by("name", "created_time"):
            grouped_views[view.folder.strip()].append(view)

        return JsonResponse(
            [
                {"name": folder_name, "views": [serialize(view) for view in views]}
                for folder_name, views in sorted(grouped_views.items())
            ]
        )
    elif request.method == "POST":
        view = View.objects.create(owner=request.user, **deserialize(request))
        return JsonResponse(serialize(view))
    else:
        return HttpResponse(status=400)


@csrf.csrf_protect
@admin_decorators.staff_member_required
def view_detail(request, pk):
    global_data.request = request
    view = get_object_or_404(get_queryset(request), pk=pk)

    if request.method == "GET":
        return JsonResponse(serialize(view))
    elif request.method == "PATCH":
        for k, v in deserialize(request).items():
            setattr(view, k, v)
        view.save()
        return JsonResponse(serialize(view))
    elif request.method == "DELETE":
        view.delete()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=400)
