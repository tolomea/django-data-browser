import functools
import logging
import math
import threading
import traceback
from copy import copy

from django import http
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property

from data_browser import version


class Settings:
    _defaults = {
        "DATA_BROWSER_ALLOW_PUBLIC": False,
        "DATA_BROWSER_AUTH_USER_COMPAT": True,
        "DATA_BROWSER_DEFAULT_ROW_LIMIT": 1000,
        "DATA_BROWSER_DEV": False,
        "DATA_BROWSER_FE_DSN": None,
        "DATA_BROWSER_ADMIN_FIELD_NAME": "admin",
        "DATA_BROWSER_USING_DB": "default",
        "DATA_BROWSER_ADMIN_OPTIONS": {},
        "DATA_BROWSER_APPS_EXPANDED": True,
        "DATA_BROWSER_ADMIN_SITE": None,
    }

    def __getattr__(self, name):
        from django.conf import settings

        if hasattr(settings, name):
            return getattr(settings, name)
        return self._defaults[name]


settings = Settings()


PUBLIC_PERM = "make_view_public"
SHARE_PERM = "share_view"


def has_permission(user, permission):
    if user is None:
        return False

    return user.has_perm(f"data_browser.{permission}")


def users_with_permission(permission):
    from data_browser.models import View

    ct = ContentType.objects.get_for_model(View)
    perm = Permission.objects.get(codename=permission, content_type=ct)
    User = get_user_model()

    qs = User.objects.none()
    for backend_path in settings.AUTHENTICATION_BACKENDS:
        qs |= User.objects.with_perm(perm, backend=backend_path)

    return qs


def str_user(user):
    return (
        str(user) or user.get_username() or getattr(user, user.get_email_field_name())
    )


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


class GlobalState(threading.local):
    def __init__(self):
        self._state = None

    @property
    def request(self):
        return self._state.request

    @property
    def models(self):
        return self._state.models


global_state = GlobalState()


class _UNSPECIFIED:
    pass


class _State:
    def __init__(
        self,
        prev,
        *,
        request=_UNSPECIFIED,
        user=_UNSPECIFIED,
        public_view=_UNSPECIFIED,
        set_ddb=True,
    ):
        if request is _UNSPECIFIED:
            request = prev.request

        new_request = copy(request)

        if user is not _UNSPECIFIED:
            new_request.user = user

        if set_ddb:
            assert public_view is not _UNSPECIFIED

            new_request.data_browser = {
                "public_view": public_view,
                "fields": set(),
                "calculated_fields": set(),
            }

        self.request = new_request
        self._children = {}

    @cached_property
    def models(self):
        from data_browser.orm_admin import get_models

        old = global_state._state
        global_state._state = None
        try:
            return get_models(self.request)
        finally:
            global_state._state = old


class set_global_state:
    def __init__(self, request=_UNSPECIFIED, **kwargs):
        self.request = request
        self.kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            assert self.request is _UNSPECIFIED
            self.request = request
            try:
                with self:
                    return func(request, *args, **kwargs)
            finally:
                self.request = _UNSPECIFIED

        return wrapper

    def __enter__(self):
        self.old = global_state._state

        cachable = self.old and self.request is _UNSPECIFIED
        key = tuple(self.kwargs.items())

        if cachable and key in self.old._children:
            state = self.old._children[key]
        else:
            state = _State(self.old, request=self.request, **self.kwargs)
            if cachable:
                self.old._children[key] = state

        global_state._state = state

    def __exit__(self, exc_type, exc_value, traceback):
        global_state._state = self.old
