from django import http

from . import version

MAKE_PUBLIC_CODENAME = "make_view_public"


def can_make_public(user):
    return user.has_perm(f"data_browser.{MAKE_PUBLIC_CODENAME}")


def JsonResponse(data):
    res = http.JsonResponse(data, safe=False)
    res["X-Version"] = version
    res["Access-Control-Expose-Headers"] = "X-Version"
    return res


def HttpResponse(*args, **kwargs):
    res = http.HttpResponse(*args, **kwargs)
    res["X-Version"] = version
    res["Access-Control-Expose-Headers"] = "X-Version"
    return res
