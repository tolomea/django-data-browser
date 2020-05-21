import os

from django.conf import settings
from django.urls import path, register_converter
from django.urls.converters import StringConverter
from django.views.generic.base import RedirectView
from django.views.static import serve

from .views import proxy_js_dev_server, query, query_ctx, query_html, view

FE_BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fe_build")


class Optional(StringConverter):
    regex = "[^/]*"


register_converter(Optional, "optional")

app_name = "data_browser"

QUERY_PATH = "query/<optional:model_name>/<optional:fields>"

urlpatterns = [
    path(f"{QUERY_PATH}.html", query_html, name="query_html"),
    path(f"{QUERY_PATH}.ctx", query_ctx, name="query_ctx"),
    path(f"{QUERY_PATH}.<media>", query, name="query"),
    path("view/<pk>.<media>", view, name="view"),
    path("", RedirectView.as_view(url="query//.html?", permanent=False), name="home"),
]
if getattr(settings, "DATA_BROWSER_DEV", False):  # pragma: no cover
    urlpatterns.append(path("<path:path>", proxy_js_dev_server))
else:
    urlpatterns.append(path("<path:path>", serve, {"document_root": FE_BUILD_DIR}))
