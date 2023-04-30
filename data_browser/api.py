import json

import django.contrib.admin.views.decorators as admin_decorators
from django.shortcuts import get_object_or_404
from django.views.decorators import csrf

from .common import (
    SHARE_PERM,
    HttpResponse,
    JsonResponse,
    add_request_info,
    str_user,
    users_with_permission,
)
from .models import View, global_data
from .orm_admin import get_models
from .query import BoundQuery
from .util import group_by


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
    ("shared", "shared", clean_noop),
]


def deserialize(request):
    data = json.loads(request.body)

    res = {
        model_field_name: clean(model_field_name, data[api_field_name])
        for model_field_name, api_field_name, clean in WRITABLE_FIELDS
        if api_field_name in data
    }

    return res


def serialize(orm_models, view):
    query = view.get_query()
    if query.model_name not in orm_models:  # pragma: no cover
        valid = False
    else:
        bound_query = BoundQuery.bind(query, orm_models)
        valid = bound_query.all_valid()

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
        "shared": bool(view.shared and view.name),
        "valid": valid,
        "can_edit": global_data.request.user == view.owner,
        "type": "view",
    }


def serialize_list(orm_models, views, *, include_invalid=False):
    res = [serialize(orm_models, view) for view in views]
    if not include_invalid:
        res = [row for row in res if row["valid"]]
    return res


def get_queryset(request):
    return View.objects.filter(owner=request.user)


def serialize_folders(orm_models, views, *, include_invalid=False):
    grouped_views = group_by(views, key=lambda v: v.folder.strip())
    flat_views = grouped_views.pop("", [])

    return serialize_list(orm_models, flat_views, include_invalid=include_invalid) + [
        {"name": folder_name, "type": "folder", "entries": entries}
        for folder_name, views in sorted(grouped_views.items())
        if (
            entries := serialize_list(
                orm_models, views, include_invalid=include_invalid
            )
        )
    ]


@csrf.csrf_protect
@admin_decorators.staff_member_required
def view_list(request):
    add_request_info(request)
    global_data.request = request
    orm_models = get_models(request)

    if request.method == "GET":
        saved_views = get_queryset(request).order_by("name", "created_time")
        shared_views = (
            View.objects.exclude(owner=request.user)
            .filter(owner__in=users_with_permission(SHARE_PERM), shared=True)
            .exclude(name="")
            .order_by("name", "created_time")
            .prefetch_related("owner")
        )

        # filter to the ones the user can view
        # shared_views = [view for view in shared_views if view.valid_for(request.user)]

        shared_views_by_user = group_by(shared_views, lambda v: str_user(v.owner))

        return JsonResponse(
            {
                "saved": serialize_folders(
                    orm_models, saved_views, include_invalid=True
                ),
                "shared": [
                    {"name": owner_name, "type": "folder", "entries": entries}
                    for owner_name, shared_views in shared_views_by_user.items()
                    if (entries := serialize_folders(orm_models, shared_views))
                ],
            }
        )
    elif request.method == "POST":
        view = View.objects.create(owner=request.user, **deserialize(request))
        return JsonResponse(serialize(orm_models, view))
    else:
        return HttpResponse(status=400)


@csrf.csrf_protect
@admin_decorators.staff_member_required
def view_detail(request, pk):
    add_request_info(request)
    global_data.request = request
    view = get_object_or_404(get_queryset(request), pk=pk)
    orm_models = get_models(request)

    if request.method == "GET":
        return JsonResponse(serialize(orm_models, view))
    elif request.method == "PATCH":
        for k, v in deserialize(request).items():
            setattr(view, k, v)
        view.save()
        return JsonResponse(serialize(orm_models, view))
    elif request.method == "DELETE":
        view.delete()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=400)
