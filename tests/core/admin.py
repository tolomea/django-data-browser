from django.contrib import admin
from django.contrib.contenttypes.admin import GenericInlineModelAdmin
from django.db.models import F

from data_browser.helpers import AdminMixin, annotation, attributes

from . import models

# admin for perm testing


class InlineAdminInline(admin.TabularInline):
    model = models.InlineAdmin
    fields = ["name"]


class GenericInlineAdminInline(GenericInlineModelAdmin):
    model = models.GenericInlineAdmin


class IgnoredAdminInline(admin.TabularInline):
    model = models.Ignored
    fields = ["name"]
    ddb_ignore = True


class NotAnAdminInline(admin.TabularInline):
    model = models.Ignored
    fields = ["name"]

    @property
    def get_queryset(self):
        raise AttributeError


@admin.register(models.Ignored)
class IgnoredAdmin(AdminMixin, admin.ModelAdmin):
    fields = ["name", "in_admin"]
    ddb_ignore = True


@admin.register(models.InAdmin)
class InAdmin(admin.ModelAdmin):
    fields = ["name"]
    inlines = [
        InlineAdminInline,
        GenericInlineAdminInline,
        IgnoredAdminInline,
        NotAnAdminInline,
    ]


@admin.register(models.Normal)
class NormalAdmin(admin.ModelAdmin):
    fields = ["name", "in_admin", "not_in_admin", "inline_admin"]


# general admin


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ["name"]


@admin.register(models.Address)
class AddressAdmin(AdminMixin, admin.ModelAdmin):
    fields = ["pk", "city", "bob", "fred", "tom", "andrew", "producer"]
    readonly_fields = ["pk", "bob", "fred", "tom", "producer"]

    def bob(self, obj):
        assert obj.street != "bad", "err"
        return "bob"

    @annotation
    def andrew(self, request, qs):
        return qs.annotate(andrew=F("street"))


class ProductMixin:
    fields = [
        "boat",
        "created_time",
        "date",
        "default_sku",
        "duration",
        "fake",
        "hidden_calculated",
        "hidden_inline",
        "hidden_model",
        "id",
        "image",
        "is_onsale",
        "model_not_in_admin",
        "name",
        "number_choice",
        "onsale",
        "producer",
        "size",
        "size_unit",
        "string_choice",
        "tags",
    ]
    readonly_fields = ["id", "is_onsale", "hidden_calculated"]
    ddb_default_filters = [
        ("a_field", "a_lookup", "a_value"),
        ("name", "not_equals", "not a thing"),
        ("a_field", "a_lookup", True),
    ]

    @attributes(ddb_hide=True)
    def hidden_calculated(self, obj):
        return obj

    @annotation
    def annotated(self, request, qs):
        return qs.annotate(annotated=F("name"))


class ProductInline(ProductMixin, admin.TabularInline):
    model = models.Product
    ddb_hide_fields = ["hidden_inline"]
    ddb_extra_fields = ["extra_inline"]


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


@attributes(short_description="funky")
def func(obj):
    return f"f{obj.name}"


def an_action(modeladmin, request, queryset):
    pass  # pragma: no cover


@attributes(ddb_hide=True)
def a_hidden_action(modeladmin, request, queryset):
    pass  # pragma: no cover


class OtherMixin:
    @annotation
    def other_annotation(self, request, qs):
        return qs.annotate(other_annotation=F("name"))


@admin.register(models.Product)
class ProductAdmin(OtherMixin, ProductMixin, AdminMixin, admin.ModelAdmin):
    inlines = [SKUInline]
    list_display = [
        "only_in_list_view",
        "annotated",
        func,
        lambda o: f"l{o.name}",
        "calculated_boolean",
    ]
    ddb_hide_fields = ["hidden_model"]
    ddb_extra_fields = ["extra_model"]
    actions = [an_action, a_hidden_action]

    @annotation
    def stealth_annotation(self, request, qs):
        return qs.annotate(stealth_annotation=F("name"))

    @annotation
    @attributes(ddb_hide=True)
    def hidden_annotation(self, request, qs):
        return qs.annotate(hidden_annotation=F("name"))

    @attributes(boolean=True)
    def calculated_boolean(self, obj):
        return obj.size
