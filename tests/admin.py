from django.contrib import admin

from . import models

# admin for perm testing


class InlineAdminInline(admin.TabularInline):
    model = models.InlineAdmin
    fields = ["name"]


@admin.register(models.InAdmin)
class InAdmin(admin.ModelAdmin):
    fields = ["name"]
    inlines = [InlineAdminInline]


@admin.register(models.Normal)
class Normal(admin.ModelAdmin):
    fields = ["name", "in_admin", "not_in_admin", "inline_admin"]


# general admin


@admin.register(models.Tag)
class Tag(admin.ModelAdmin):
    fields = ["name"]


@admin.register(models.Address)
class Address(admin.ModelAdmin):
    fields = ["pk", "city", "bob", "fred", "tom"]
    readonly_fields = ["bob", "fred", "tom"]

    def bob(self, obj):
        assert obj.street != "bad", obj.street
        return "bob"


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
    readonly_fields = ["is_onsale"]


class ProductInline(ProductMixin, admin.TabularInline):
    model = models.Product


@admin.register(models.Producer)
class Producer(admin.ModelAdmin):
    fields = ["name", "address"]
    inlines = [ProductInline]


class SKUInline(admin.TabularInline):
    model = models.SKU
    fields = ["name", "product", "bob"]
    readonly_fields = ["bob"]

    def bob(self, obj):  # pragma: no cover don't show funcs on inlines test
        return "bob"


@admin.register(models.Product)
class Product(ProductMixin, admin.ModelAdmin):
    inlines = [SKUInline]
    list_display = ["only_in_list_view"]
