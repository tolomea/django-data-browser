import os

from django.urls import path, re_path, register_converter
from django.urls.converters import StringConverter
from django.views.generic.base import RedirectView
from django.views.static import serve

from .api import view_detail, view_list
from .common import settings
from .views import proxy_js_dev_server, query, query_ctx, query_html, view

FE_BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fe_build")
WEB_ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_root")


class OptionalString(StringConverter):
    regex = "[^/]*"


register_converter(OptionalString, "opt_str")


app_name = "data_browser"

QUERY_PATH = "query/<model_name>/<opt_str:fields>"

if settings.DATA_BROWSER_DEV:  # pragma: no cover
    static_view = (proxy_js_dev_server,)
else:
    static_view = (serve, {"document_root": FE_BUILD_DIR})

urlpatterns = [
    # queries
    path(f"{QUERY_PATH}.html", query_html, name="query_html"),
    path(f"{QUERY_PATH}.ctx", query_ctx),
    path(f"{QUERY_PATH}.<media>", query, name="query"),
    # views
    path("view/<pk>.<media>", view, name="view"),
    # api
    path("api/views/", view_list, name="view_list"),
    path("api/views/<pk>/", view_detail, name="view_detail"),
    # other html pages
    re_path(r".*\.html", query_html),
    re_path(r".*\.ctx", query_ctx),
    path("", query_html, name="home"),
    # static files
    re_path(r"^(?P<path>static/.*)$", *static_view, name="static"),
    re_path(
        r"^.*/(?P<path>static/.*)$",
        RedirectView.as_view(pattern_name="data_browser:static", permanent=True),
    ),
    re_path(r"^(?P<path>.*)$", serve, {"document_root": WEB_ROOT_DIR}),
]
