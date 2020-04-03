from django.urls import path, re_path, register_converter

from .views import catchall, query, view


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
    re_path("", catchall),
]
