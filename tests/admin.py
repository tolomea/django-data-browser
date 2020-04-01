from django.contrib import admin

from . import models


@admin.register(models.InAdmin)
class InAdmin(admin.ModelAdmin):
    fields = ["name"]


@admin.register(models.Tag)
class Tag(admin.ModelAdmin):
    fields = ["name"]


@admin.register(models.Address)
class Address(admin.ModelAdmin):
    fields = ["city"]


class ProductMixin:
    fields = [
        "pk",
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
    ]
    readonly_fields = ["is_onsale"]


class ProductInline(ProductMixin, admin.TabularInline):
    model = models.Product


@admin.register(models.Producer)
class Producer(admin.ModelAdmin):
    fields = ["name", "address"]
    inlines = [ProductInline]


class SKUMixin:
    fields = ["name", "product"]


class SKUInline(SKUMixin, admin.TabularInline):
    model = models.SKU


@admin.register(models.Product)
class Product(ProductMixin, admin.ModelAdmin):
    inlines = [SKUInline]


@admin.register(models.SKU)
class SKU(SKUMixin, admin.ModelAdmin):
    pass
