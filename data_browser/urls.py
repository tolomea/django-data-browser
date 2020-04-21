import os

from django.conf import settings
from django.urls import path, register_converter
from django.views.static import serve

from .views import proxy_js_dev_server, query, query_html, view

FE_BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fe_build")


class Optional:
    regex = "[^/]*"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(Optional, "optional")

app_name = "data_browser"

urlpatterns = [
    path("query/<app>/<model>/<optional:fields>.html", query_html, name="query_html"),
    path("query/<app>/<model>/<optional:fields>.<media>", query, name="query"),
    path("view/<pk>.<media>", view, name="view"),
    path("", lambda: None, name="root"),
]
if getattr(settings, "DATA_BROWSER_DEV", False):  # pragma: no cover
    urlpatterns.append(path("<path:path>", proxy_js_dev_server))
else:
    urlpatterns.append(path("<path:path>", serve, {"document_root": FE_BUILD_DIR}))
