from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.utils.html import format_html

from . import models
from .common import can_make_public
from .helpers import AdminMixin


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
