from django.contrib import admin
from django.contrib.contenttypes.admin import GenericInlineModelAdmin
from django.db.models import F

from data_browser.helpers import AdminMixin, annotation

from . import models

# admin for perm testing


class InlineAdminInline(admin.TabularInline):
    model = models.InlineAdmin
    fields = ["name"]


class GenericInlineAdminInline(GenericInlineModelAdmin):
    model = models.GenericInlineAdmin


@admin.register(models.InAdmin)
class InAdmin(admin.ModelAdmin):
    fields = ["name"]
    inlines = [InlineAdminInline, GenericInlineAdminInline]


@admin.register(models.Normal)
class NormalAdmin(admin.ModelAdmin):
    fields = ["name", "in_admin", "not_in_admin", "inline_admin"]


# general admin


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ["name"]


@admin.register(models.Address)
class AddressAdmin(AdminMixin, admin.ModelAdmin):
    fields = ["pk", "city", "bob", "fred", "tom", "andrew"]
    readonly_fields = ["pk", "bob", "fred", "tom"]

    def bob(self, obj):
        assert obj.street != "bad", "err"
        return "bob"

    @annotation
    def andrew(self, request, qs):
        return qs.annotate(andrew=F("street"))


class ProductMixin:
    fields = [
        "id",
        "producer",
        "name",
        "size",
        "size_unit",
        "producer",
        "is_onsale",
        "default_sku",
        "tags",
        "model_not_in_admin",
        "onsale",
        "image",
        "created_time",
    ]
    readonly_fields = ["id", "is_onsale"]


class ProductInline(ProductMixin, admin.TabularInline):
    model = models.Product


@admin.register(models.Producer)
class ProducerAdmin(admin.ModelAdmin):
    fields = ["name", "address", "frank"]
    readonly_fields = ["frank"]
    inlines = [ProductInline]

    def frank(self, obj):
        return "frank"


class SKUInline(admin.TabularInline):
    model = models.SKU
    fields = ["name", "product", "bob"]
    readonly_fields = ["bob"]

    def bob(self, obj):  # pragma: no cover don't show funcs on inlines test
        return "bob"


@admin.register(models.Product)
class ProductAdmin(AdminMixin, ProductMixin, admin.ModelAdmin):
    inlines = [SKUInline]
    list_display = ["only_in_list_view", "annotated"]

    @annotation
    def annotated(self, request, qs):
        return qs.annotate(annotated=F("name"))
