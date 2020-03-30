from django.conf import settings
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from . import models


@admin.register(models.View)
class ViewAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "owner",
                    "public",
                    "open_view",
                    "public_link",
                    "google_sheets_formula",
                    "description",
                ]
            },
        ),
        ("Query", {"fields": [("app", "model"), "fields", "query"]}),
        ("Internal", {"fields": ["id", "created_time"]}),
    ]
    readonly_fields = ["open_view", "public_link", "google_sheets_formula", "id"]
    list_display = ["__str__", "owner", "public"]

    def get_readonly_fields(self, request, obj=None):
        res = list(super().get_readonly_fields(request, obj))
        if obj:
            res.extend(["app", "model", "fields", "query"])
        return res

    def open_view(self, obj):
        url = obj.get_query("html").url
        return format_html(f'<a href="{url}">view</a>')

    def public_link(self, obj):
        if obj.public:
            url = reverse("data_browser:view", kwargs={"pk": obj.pk, "media": "csv"})
            return f"{settings.WEBSITE_BASE}{url}"
        else:
            return "N/A"

    def google_sheets_formula(self, obj):
        if obj.public:
            url = reverse("data_browser:view", kwargs={"pk": obj.pk, "media": "csv"})
            return f'=importdata("{settings.WEBSITE_BASE}{url}")'
        else:
            return "N/A"

    def get_changeform_initial_data(self, request):
        get_data = super().get_changeform_initial_data(request)
        get_data["owner"] = request.user.pk
        return get_data
