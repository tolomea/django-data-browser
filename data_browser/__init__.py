from pathlib import Path

version = "4.2.14"

_FE_BUILD_DIR = Path(__file__).resolve().parent / "fe_build"
_WEB_ROOT_DIR = Path(__file__).resolve().parent / "web_root"

_converter_registered = False


def _register_url_converter():
    global _converter_registered
    if _converter_registered:  # pragma: no cover
        return
    from django.urls import register_converter
    from django.urls.converters import StringConverter

    class _OptionalString(StringConverter):
        regex = "[^/]*"

    register_converter(_OptionalString, "opt_str")
    _converter_registered = True


def get_urls(admin_site=None, **setting_overrides):
    _register_url_converter()

    from django.core.exceptions import ImproperlyConfigured
    from django.urls import include
    from django.urls import path
    from django.urls import re_path
    from django.views.generic.base import RedirectView
    from django.views.static import serve

    from data_browser.api import view_detail
    from data_browser.api import view_list
    from data_browser.common import InstanceSettings
    from data_browser.common import _registry
    from data_browser.common import _resolve_admin_site
    from data_browser.common import settings
    from data_browser.views import proxy_js_dev_server
    from data_browser.views import query
    from data_browser.views import query_ctx
    from data_browser.views import query_html
    from data_browser.views import view

    if admin_site is None:
        admin_site = _resolve_admin_site(settings.DATA_BROWSER_ADMIN_SITE)
        namespace = "data_browser"
    else:
        admin_site = _resolve_admin_site(admin_site)
        namespace = f"data_browser_{admin_site.name}"

    if namespace in _registry:
        raise ImproperlyConfigured(
            f"Data browser already registered for admin site '{admin_site.name}'"
        )

    overrides = {f"DATA_BROWSER_{k.upper()}": v for k, v in setting_overrides.items()}
    overrides["DATA_BROWSER_ADMIN_SITE"] = admin_site
    instance_settings = InstanceSettings(namespace, overrides)
    _registry[namespace] = instance_settings

    if instance_settings.DATA_BROWSER_DEV:  # pragma: no cover
        static_view = (proxy_js_dev_server,)
    else:
        static_view = (serve, {"document_root": _FE_BUILD_DIR})

    query_path = "query/<model_name>/<opt_str:fields>"
    query_html_view = admin_site.admin_view(query_html)
    query_ctx_view = admin_site.admin_view(query_ctx)

    patterns = [
        # queries
        path(f"{query_path}.html", query_html_view, name="query_html"),
        path(f"{query_path}.ctx", query_ctx_view),
        path(f"{query_path}.<media>", admin_site.admin_view(query), name="query"),
        # views
        path("view/<pk>.<media>", view, name="view"),
        # api
        path("api/views/", admin_site.admin_view(view_list), name="view_list"),
        path("api/views/<pk>/", admin_site.admin_view(view_detail), name="view_detail"),
        # other html pages
        re_path(r".*\.html", query_html_view),
        re_path(r".*\.ctx", query_ctx_view),
        path("", query_html_view, name="home"),
        # static files
        re_path(r"^(?P<path>static/.*)$", *static_view, name="static"),
        re_path(
            r"^.*/(?P<path>static/.*)$",
            RedirectView.as_view(pattern_name=f"{namespace}:static", permanent=True),
        ),
        re_path(r"^(?P<path>.*)$", serve, {"document_root": _WEB_ROOT_DIR}),
    ]

    return include((patterns, "data_browser"), namespace=namespace)
