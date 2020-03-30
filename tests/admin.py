from django.contrib import admin

from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ["pk", "name", "size", "size_unit", "producer", "is_onsale"]
    readonly_fields = ["is_onsale"]


@admin.register(models.Producer)
class Producer(admin.ModelAdmin):
    fields = ["name"]
