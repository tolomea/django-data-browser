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
        ("Internal", {"fields": ["id", "created_time", "shared", "admin_site"]}),
    ]
    list_display = ["__str__", "owner", "public", "admin_site"]
    list_filter = ["admin_site"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_fieldsets(self, request, obj=None):
        res = super().get_fieldsets(request, obj)
        if not has_permission(request.user, PUBLIC_PERM):
            res = [fs for fs in res if fs[0] != "Public"]
        return res

    def changeform_view(self, request, object_id=None, *args, **kwargs):
        site_name = None
        if object_id is not None:
            view_obj = models.View.objects.get(pk=object_id)
            site_name = view_obj.admin_site
        with set_global_state(
            request=request, set_ddb=False, admin_site_name=site_name
        ):
            res = super().changeform_view(request, object_id, *args, **kwargs)
            res.render()
        return res

    @staticmethod
    def open_view(obj):
        if not obj.model_name:
            return "N/A"  # pragma: no cover
        return format_html('<a href="{}">view</a>', obj.url)

    @attributes(boolean=True)
    def valid(self, obj):
        with set_global_state(
            override_request_user=obj.owner,
            public_view=False,
            admin_site_name=obj.admin_site,
        ):
            return obj.is_valid()
