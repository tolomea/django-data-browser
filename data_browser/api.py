import json

import django.contrib.admin.views.decorators as admin_decorators
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from .common import can_make_public
from .models import View


def deserialize(request):
    data = json.loads(request.body)
    if "model" in data:
        data["model_name"] = data.pop("model")

    res = {
        f: data[f]
        for f in ["name", "description", "public", "model_name", "fields", "query"]
        if f in data
    }

    if not can_make_public(request.user):
        res["public"] = False
    return res


def serialize(view):
    return {
        "name": view.name,
        "description": view.description,
        "public": view.public,
        "model": view.model_name,
        "fields": view.fields,
        "query": view.query,
        # public link fields
    }


def get_queryset(request):
    return View.objects.filter(owner=request.user)


@admin_decorators.staff_member_required
def view_list(request):
    if request.method == "GET":
        return JsonResponse(
            [serialize(view) for view in get_queryset(request).order_by("name")],
            safe=False,
        )
    elif request.method == "POST":
        view = View.objects.create(owner=request.user, **deserialize(request))
        return JsonResponse(serialize(view))
    else:
        return HttpResponse(status=400)


@admin_decorators.staff_member_required
def view_detail(request, pk):
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
