from django.urls import path, register_converter

from .views import query, view


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
    path(fr"view/<pk>.<media>", view, name="view"),
]
