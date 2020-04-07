import os

from django.conf import settings
from django.urls import path, re_path, register_converter
from django.views.static import serve

from .views import QueryHTML, catchall_proxy, query, query_html_proxy, view

FE_BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fe_build")


class Optional:
    regex = "[^/]*"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(Optional, "optional")

app_name = "data_browser"

if getattr(settings, "DATA_BROWSER_DEV", False):
    urlpatterns = [
        path(
            "query/<app>/<model>/<optional:fields>.bob",
            query_html_proxy,
            name="query_html",
        ),
        path("query/<app>/<model>/<optional:fields>.<media>", query, name="query"),
        path("view/<pk>.<media>", view, name="view"),
        re_path(r"^(?P<path>.*)$", catchall_proxy),
    ]
else:
    urlpatterns = [
        path(
            "query/<app>/<model>/<optional:fields>.bob",
            QueryHTML.as_view(),
            name="query_html",
        ),
        path("query/<app>/<model>/<optional:fields>.<media>", query, name="query"),
        path("view/<pk>.<media>", view, name="view"),
        path("<path:path>", serve, {"document_root": FE_BUILD_DIR}),
    ]
