from django.contrib import admin
from django.utils.html import format_html

from data_browser import models
from data_browser.common import PUBLIC_PERM
from data_browser.common import has_permission
from data_browser.common import set_global_state
from data_browser.helpers import AdminMixin
from data_browser.helpers import attributes


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

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_fieldsets(self, request, obj=None):
        res = super().get_fieldsets(request, obj)
        if not has_permission(request.user, PUBLIC_PERM):
            res = [fs for fs in res if fs[0] != "Public"]
        return res

    def changeform_view(self, request, *args, **kwargs):
        with set_global_state(request=request, set_ddb=False):
            res = super().changeform_view(request, *args, **kwargs)
            res.render()
        return res

    @staticmethod
    def open_view(obj):
        if not obj.model_name:
            return "N/A"  # pragma: no cover
        return format_html(f'<a href="{obj.url}">view</a>')

    @attributes(boolean=True)
    def valid(self, obj):
        with set_global_state(user=obj.owner, public_view=False):
            return obj.is_valid()
