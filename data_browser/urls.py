import os

from django.conf import settings
from django.urls import path, re_path, register_converter
from django.views.static import serve

from .views import Index, catchall, query, view

FE_BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fe_build")
assert os.stat(FE_BUILD_DIR)


class Optional:
    regex = "[^/]*"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(Optional, "optional")

app_name = "data_browser"

urlpatterns = [
    path("query/<app>/<model>/<optional:fields>.<media>", query, name="query"),
    path("view/<pk>.<media>", view, name="view"),
]

if getattr(settings, "DATA_BROWSER_DEV", False):
    urlpatterns += [re_path(r"^(?P<path>.*)$", catchall)]
else:
    urlpatterns += [
        path("", Index.as_view(), name="index"),
        path("<path:path>", serve, {"document_root": FE_BUILD_DIR}),
    ]
