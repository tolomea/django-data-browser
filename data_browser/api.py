import json

from django.shortcuts import get_object_or_404

from data_browser.common import SHARE_PERM
from data_browser.common import HttpResponse
from data_browser.common import JsonResponse
from data_browser.common import global_state
from data_browser.common import set_global_state
from data_browser.common import str_user
from data_browser.common import users_with_permission
from data_browser.models import View
from data_browser.util import group_by


def _get_admin_site_name():
    return global_state.settings.DATA_BROWSER_ADMIN_SITE.name


def clean_str(field, value):
    return value.strip()[: View._meta.get_field(field).max_length]


def clean_uint(field, value):
    try:
        value = int(value)
    except Exception:
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


def deserialize(data):
    res = {
        model_field_name: clean(model_field_name, data[api_field_name])
        for model_field_name, api_field_name, clean in WRITABLE_FIELDS
        if api_field_name in data
    }

    return res


def name_sort(entries):
    return sorted(entries, key=lambda entry: entry["name"].lower())


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
        "shared": bool(view.shared and view.name),
        "valid": view.is_valid(),
        "can_edit": global_state.request.user == view.owner,
        "type": "view",
    }


def serialize_list(views, *, include_invalid=False):
    res = [serialize(view) for view in views]
    if not include_invalid:
        res = [row for row in res if row["valid"]]
    return name_sort(res)


def serialize_folders(views, *, include_invalid=False):
    grouped_views = group_by(views, key=lambda v: v.folder.strip())
    flat_views = grouped_views.pop("", [])

    res = serialize_list(flat_views, include_invalid=include_invalid)
    for folder_name, views in sorted(grouped_views.items()):
        entries = serialize_list(views, include_invalid=include_invalid)
        if entries:
            res.append({"name": folder_name, "type": "folder", "entries": entries})
    return name_sort(res)


def get_queryset(user):
    admin_site_name = global_state.settings.DATA_BROWSER_ADMIN_SITE.name
    return View.objects.filter(owner=user, admin_site=admin_site_name)


@set_global_state(public_view=False)
def view_list(request):
    if request.method == "GET":
        admin_site_name = global_state.settings.DATA_BROWSER_ADMIN_SITE.name

        # saved
        saved_views = get_queryset(request.user)
        saved_views_serialized = serialize_folders(saved_views, include_invalid=True)

        # shared
        shared_views = (
            View.objects
            .filter(admin_site=admin_site_name)
            .exclude(owner=request.user)
            .filter(owner__in=users_with_permission(SHARE_PERM), shared=True)
            .exclude(name="")
            .prefetch_related("owner")
        )
        shared_views_by_user = group_by(shared_views, lambda v: str_user(v.owner))
        shared_views_serialized = []
        for owner_name, shared_views in shared_views_by_user.items():
            entries = serialize_folders(shared_views)
            if entries:
                shared_views_serialized.append({
                    "name": owner_name,
                    "type": "folder",
                    "entries": entries,
                })

        # response
        return JsonResponse({
            "saved": saved_views_serialized,
            "shared": shared_views_serialized,
        })
    elif request.method == "POST":
        data = json.loads(request.body)
        view = View.objects.create(
            owner=request.user, admin_site=_get_admin_site_name(), **deserialize(data)
        )
        return JsonResponse(serialize(view))
    else:
        return HttpResponse(status=400)


@set_global_state(public_view=False)
def view_detail(request, pk):
    view = get_object_or_404(get_queryset(request.user), pk=pk)

    if request.method == "GET":
        return JsonResponse(serialize(view))
    elif request.method == "PATCH":
        data = json.loads(request.body)
        for k, v in deserialize(data).items():
            setattr(view, k, v)
        view.save()
        return JsonResponse(serialize(view))
    elif request.method == "DELETE":
        view.delete()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=400)
