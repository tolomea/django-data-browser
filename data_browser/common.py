import logging
import math
import traceback

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


def debug_log(msg, exc=None):  # pragma: no cover
    if exc:
        if isinstance(exc, AssertionError):
            raise
        msg = f"{msg}:\n{traceback.format_exc()}"

    if settings.DEBUG:
        logging.getLogger(__name__).warning(f"DDB: {msg}")


def all_subclasses(cls):
    res = set()
    queue = {cls}
    while queue:
        cls = queue.pop()
        subs = set(cls.__subclasses__())
        queue.update(subs - res)
        res.update(subs)
    return res


def get_optimal_decimal_places(nums, sf=3, max_dp=6):
    actual_dps = set()
    filtered = set()
    for num in nums:
        if num:
            s = f"{num:g}"
            filtered.add(num)
            if "e-" in s:
                actual_dps.add(float("inf"))
            elif "." in s:
                actual_dps.add(len(s.split(".")[1]))
            else:
                actual_dps.add(0)

    if not filtered:
        return 0

    max_actual_dp = max(actual_dps)
    if max_actual_dp <= 2:
        return max_actual_dp

    min_value = min(filtered)
    min_magnitude = math.floor(math.log(min_value, 10))
    dp_for_sf = sf - min_magnitude - 1

    return max(0, min(dp_for_sf, max_actual_dp, max_dp))


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
