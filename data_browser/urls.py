import os

from django.conf import settings
from django.urls import path, re_path, register_converter
from django.urls.converters import StringConverter
from django.views.generic.base import RedirectView
from django.views.static import serve

from .views import proxy_js_dev_server, query, query_ctx, query_html, view

FE_BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fe_build")
WEB_ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_root")


class Optional(StringConverter):
    regex = "[^/]*"


register_converter(Optional, "optional")

app_name = "data_browser"

QUERY_PATH = "query/<optional:model_name>/<optional:fields>"

if getattr(settings, "DATA_BROWSER_DEV", False):  # pragma: no cover
    static_view = (proxy_js_dev_server,)
else:
    static_view = (serve, {"document_root": FE_BUILD_DIR})

urlpatterns = [
    path(f"{QUERY_PATH}.html", query_html, name="query_html"),
    path(f"{QUERY_PATH}.ctx", query_ctx, name="query_ctx"),
    path(f"{QUERY_PATH}.<media>", query, name="query"),
    path("view/<pk>.<media>", view, name="view"),
    path("", query_html, name="home"),
    # hook up the static file serving
    re_path(r"^(?P<path>static/.*)$", *static_view),
    re_path(
        r"^.*/(?P<path>static/.*)$",
        RedirectView.as_view(pattern_name="data_browser:static", permanent=True),
    ),
    re_path(r"^(?P<path>.*)$", serve, {"document_root": WEB_ROOT_DIR}),
]
