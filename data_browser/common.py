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


class Settings:
    _defaults = {
        "DATA_BROWSER_ALLOW_PUBLIC": False,
        "DATA_BROWSER_AUTH_USER_COMPAT": True,
        "DATA_BROWSER_DEFAULT_ROW_LIMIT": 1000,
        "DATA_BROWSER_DEV": False,
        "DATA_BROWSER_FE_DSN": None,
    }

    def __getattr__(self, name):
        from django.conf import settings

        if hasattr(settings, name):
            return getattr(settings, name)
        return self._defaults[name]


settings = Settings()
