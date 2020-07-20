from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.utils.html import format_html

from . import models
from .common import can_make_public


class AdminMixin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        for annotation in getattr(self, "_DDB_annotations", {}).values():
            qs = annotation.get_queryset(self, request, qs)
        return qs


class AnnotationDescriptor:
    def __init__(self, annotated_field_name, get_queryset):
        self.admin_order_field = annotated_field_name
        self.get_queryset = get_queryset

    def __set_name__(self, owner, name):
        self.__name__ = name
        if not issubclass(owner, AdminMixin):  # pragma: no cover
            raise Exception(
                "Django Data Browser 'annotation' decorator used without 'AdminMixin'"
            )
        if not hasattr(owner, "_DDB_annotations"):  # pragma: no branch
            owner._DDB_annotations = {}
        owner._DDB_annotations[name] = self

    def __get__(self, instance, owner=None):
        return self

    def __call__(self, obj):  # pragma: no cover
        return getattr(obj, self.admin_order_field)


def annotation(annotated_field_name):
    if callable(annotated_field_name):  # pragma: no cover
        raise TypeError(
            "annotation() missing 1 required positional argument: 'annotated_field_name'"
        )

    def decorator(func):
        return AnnotationDescriptor(annotated_field_name, func)

    return decorator


@admin.register(models.View)
class ViewAdmin(AdminMixin, admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name", "owner", "open_view", "description"]}),
        (
            "Public",
            {
                "fields": [
                    "public",
                    "public_slug",
                    "public_link",
                    "google_sheets_formula",
                ]
            },
        ),
        ("Query", {"fields": ["model_name", "fields", "query", "limit"]}),
        ("Internal", {"fields": ["id", "created_time"]}),
    ]
    list_display = ["__str__", "owner", "public"]

    def get_readonly_fields(self, request, obj):
        return flatten_fieldsets(self.get_fieldsets(request, obj))

    def get_fieldsets(self, request, obj=None):
        res = super().get_fieldsets(request, obj)
        if not can_make_public(request.user):
            res = [fs for fs in res if fs[0] != "Public"]
        return res

    def change_view(self, request, *args, **kwargs):
        models.global_data.request = request
        return super().change_view(request, *args, **kwargs)

    @staticmethod
    def open_view(obj):
        if not obj.model_name:
            return "N/A"
        url = obj.get_query().get_url("html")
        return format_html(f'<a href="{url}">view</a>')

    def get_changeform_initial_data(self, request):
        get_results = super().get_changeform_initial_data(request)
        get_results["owner"] = request.user.pk
        return get_results
