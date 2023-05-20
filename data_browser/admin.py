from copy import copy

from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.utils.html import format_html

from . import models
from .common import PUBLIC_PERM, add_request_info, has_permission
from .helpers import AdminMixin, attributes
from .orm_admin import get_models


@admin.register(models.View)
class ViewAdmin(AdminMixin, admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "owner",
                    "valid",
                    "open_view",
                    "folder",
                    "description",
                ]
            },
        ),
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
        ("Internal", {"fields": ["id", "created_time", "shared"]}),
    ]
    list_display = ["__str__", "owner", "public"]

    def get_readonly_fields(self, request, obj):
        return flatten_fieldsets(self.get_fieldsets(request, obj))

    def get_fieldsets(self, request, obj=None):
        res = super().get_fieldsets(request, obj)
        if not has_permission(request.user, PUBLIC_PERM):
            res = [fs for fs in res if fs[0] != "Public"]
        return res

    def get_object(self, request, object_id, from_field=None):
        res = super().get_object(request, object_id, from_field=from_field)

        ddb_request = copy(request)
        ddb_request.environ = request.environ
        ddb_request.user = res.owner
        add_request_info(ddb_request)
        models.global_data.request = ddb_request

        return res

    @staticmethod
    def open_view(obj):
        if not obj.model_name:
            return "N/A"
        return format_html(f'<a href="{obj.url}">view</a>')

    @attributes(boolean=True)
    def valid(self, obj):
        orm_models = get_models(models.global_data.request)
        return obj.get_query().is_valid(orm_models)

    def get_changeform_initial_data(self, request):
        get_results = super().get_changeform_initial_data(request)
        get_results["owner"] = request.user.pk
        return get_results
