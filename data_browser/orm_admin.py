from collections import defaultdict

from django.contrib.admin import site
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.db.models.fields.reverse_related import ForeignObjectRel, OneToOneRel
from django.forms.models import _get_foreign_key
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify

from .common import debug_log, settings
from .helpers import AdminMixin, AnnotationDescriptor, attributes
from .orm_fields import (
    OrmAnnotatedField,
    OrmCalculatedField,
    OrmConcreteField,
    OrmFileField,
    OrmFkField,
    OrmModel,
    get_fields_for_type,
    get_model_name,
)
from .types import (
    TYPES,
    BooleanType,
    DateTimeType,
    DateType,
    DurationType,
    JSONType,
    NumberArrayType,
    NumberChoiceType,
    NumberType,
    StringArrayType,
    StringChoiceType,
    StringType,
    UnknownType,
)

try:
    from django.contrib.postgres.fields import ArrayField
except ModuleNotFoundError:  # pragma: postgres
    ArrayField = None.__class__

try:
    from django.db.models import JSONField
except ImportError:  # pragma: django < 3.1
    try:
        from django.contrib.postgres.fields import JSONField
    except ModuleNotFoundError:  # pragma: postgres
        JSONField = None.__class__


OPEN_IN_ADMIN = "admin"

_STRING_FIELDS = (
    models.CharField,
    models.TextField,
    models.GenericIPAddressField,
    models.UUIDField,
)
_NUMBER_FIELDS = (
    models.DecimalField,
    models.FloatField,
    models.IntegerField,
    models.AutoField,
)
_FIELD_TYPE_MAP = {
    models.BooleanField: BooleanType,
    models.DurationField: DurationType,
    models.NullBooleanField: BooleanType,
    models.DateTimeField: DateTimeType,
    models.DateField: DateType,
    **{f: StringType for f in _STRING_FIELDS},
    **{f: NumberType for f in _NUMBER_FIELDS},
}


@attributes(short_description=OPEN_IN_ADMIN)
def open_in_admin(obj):
    if obj is None:  # pragma: no cover
        return None

    model_name = get_model_name(obj.__class__, "_")
    url_name = f"admin:{model_name}_change".lower()
    url = reverse(url_name, args=[obj.pk])
    return format_html('<a href="{}">{}</a>', url, obj)


def admin_get_queryset(admin, request, fields=()):
    request.data_browser = {"calculated_fields": set(fields), "fields": set(fields)}
    return admin.get_queryset(request)


def _get_all_admin_fields(request):
    request.data_browser = {"calculated_fields": set(), "fields": set()}

    def from_fieldsets(admin, all_):
        auth_user_compat = settings.DATA_BROWSER_AUTH_USER_COMPAT
        if auth_user_compat and isinstance(admin, UserAdmin):
            obj = admin.model()  # get the change fieldsets, not the add ones
        else:
            obj = None

        fields = admin.get_fieldsets(request, obj)
        for f in flatten_fieldsets(fields):
            # skip calculated fields on inlines
            if not isinstance(admin, InlineModelAdmin) or hasattr(admin.model, f):
                yield f

    def visible(model_admin, request):
        attrs = ["get_fieldsets", "model", "get_queryset"]
        if not all(hasattr(model_admin, a) for a in attrs):
            debug_log(
                f"{type(model_admin)} instance does not look like a ModelAdmin or InlineModelAdmin"
            )
            return False
        if getattr(model_admin, "ddb_ignore", False):
            return False
        if model_admin.has_change_permission(request):
            return True
        if hasattr(model_admin, "has_view_permission"):
            return model_admin.has_view_permission(request)
        else:
            return False  # pragma: no cover  Django < 2.1

    all_admin_fields = defaultdict(set)
    hidden_fields = defaultdict(set)
    model_admins = {}
    for model, model_admin in site._registry.items():
        model_admins[model] = model_admin
        if visible(model_admin, request):
            all_admin_fields[model].update(from_fieldsets(model_admin, True))
            all_admin_fields[model].update(model_admin.get_list_display(request))
            all_admin_fields[model].update(getattr(model_admin, "ddb_extra_fields", []))
            all_admin_fields[model].add(open_in_admin)
            hidden_fields[model].update(getattr(model_admin, "ddb_hide_fields", []))

            # check the inlines, these are already filtered for access
            for inline in model_admin.get_inline_instances(request):
                if visible(inline, request):
                    try:
                        fk_field = _get_foreign_key(model, inline.model, inline.fk_name)
                    except Exception as e:
                        debug_log(e)  # ignore things like GenericInlineModelAdmin
                    else:
                        if inline.model not in model_admins:  # pragma: no branch
                            model_admins[inline.model] = inline
                        all_admin_fields[inline.model].update(
                            from_fieldsets(inline, False)
                        )
                        all_admin_fields[inline.model].update(
                            getattr(inline, "ddb_extra_fields", [])
                        )
                        all_admin_fields[inline.model].add(fk_field.name)
                        hidden_fields[inline.model].update(
                            getattr(inline, "ddb_hide_fields", [])
                        )

    for model, model_admin in model_admins.items():
        if isinstance(model_admin, AdminMixin):
            all_admin_fields[model].update(model_admin._ddb_annotations())

    # we always have id and never pk
    for fields in all_admin_fields.values():
        fields.add("id")
        fields.discard("pk")
        fields.discard("__str__")

    # throw away the hidden ones
    for model, fields in hidden_fields.items():
        for f in fields:
            all_admin_fields[model].discard(f)

    return model_admins, all_admin_fields


def _get_calculated_field(request, field_name, model_name, model, admin, model_fields):
    if isinstance(field_name, str):
        field_func = getattr(admin, field_name, None)
    else:
        field_func = field_name
        field_name = getattr(
            field_func, "short_description", slugify(str(field_func.__name__))
        )

    if isinstance(field_func, AnnotationDescriptor):
        qs = admin_get_queryset(admin, request, [field_name])

        annotation = qs.query.annotations.get(field_name)
        if not annotation:  # pragma: no cover
            raise Exception(
                f"Can't find annotation '{field_name}' for {admin}.{field_name}"
            )

        field_type = getattr(annotation, "output_field", None)
        if not field_type:  # pragma: no cover
            raise Exception(
                f"Annotation '{field_name}' for {admin}.{field_name} doesn't specify 'output_field'"
            )

        type_, choices = _get_field_type(model, field_name, field_type)
        return OrmAnnotatedField(
            model_name=model_name,
            name=field_name,
            pretty_name=field_name,
            type_=type_,
            field_type=field_type,
            admin=admin,
            choices=choices,
        )
    else:
        if getattr(field_func, "ddb_hide", False):
            return None

        if field_func is None:

            def field_func(obj):
                value = getattr(obj, field_name)
                return value() if callable(value) else value

        return OrmCalculatedField(
            model_name=model_name,
            name=field_name,
            pretty_name=field_name,
            func=field_func,
        )


def _fmt_choices(choices):
    return [(value, str(label)) for value, label in choices or []]


def _get_field_type(model, field_name, field):
    if isinstance(field, ArrayField) and isinstance(
        field.base_field, _STRING_FIELDS
    ):  # pragma: postgres
        return StringArrayType, _fmt_choices(field.base_field.choices)
    elif isinstance(field, ArrayField) and isinstance(
        field.base_field, _NUMBER_FIELDS
    ):  # pragma: postgres
        return NumberArrayType, _fmt_choices(field.base_field.choices)
    elif isinstance(field, JSONField):
        res = JSONType
    elif field.__class__ in _FIELD_TYPE_MAP:
        res = _FIELD_TYPE_MAP[field.__class__]
    else:
        for django_type, field_type in _FIELD_TYPE_MAP.items():
            if isinstance(field, django_type):
                res = field_type
                break
        else:
            debug_log(
                f"{model.__name__}.{field_name} unsupported type {type(field).__name__}"
            )
            res = UnknownType

    # Choice fields have different lookups
    if res is StringType and field.choices:
        return StringChoiceType, _fmt_choices(field.choices)
    elif res is NumberType and field.choices:
        return NumberChoiceType, _fmt_choices(field.choices)
    else:
        return res, None


def _make_json_sub_module(model_name, field_types):
    TYPE_MAP = {"string": StringType, "number": NumberType, "boolean": BooleanType}

    fields = dict(get_fields_for_type(JSONType))
    for field_name, type_name in field_types.items():
        type_ = TYPE_MAP[type_name]
        fields[field_name] = OrmConcreteField(
            model_name=model_name,
            name=field_name,
            pretty_name=field_name,
            type_=type_,
            rel_name=type_.name,
        )

    return OrmModel(fields)


def _get_fields_for_model(request, model, admin, admin_fields):
    fields = {}
    orm_models = {}

    model_name = get_model_name(model)
    model_fields = {f.name: f for f in model._meta.get_fields()}

    for field_name in admin_fields[model]:
        field = model_fields.get(field_name)
        if isinstance(field, (models.ForeignKey, OneToOneRel)):
            if field.related_model in admin_fields:
                fields[field_name] = OrmFkField(
                    model_name=model_name,
                    name=field_name,
                    pretty_name=field_name,
                    rel_name=get_model_name(field.related_model),
                )
        elif isinstance(field, (ForeignObjectRel, models.ManyToManyField)):
            pass  # TODO 2many support
        elif isinstance(field, models.FileField):
            fields[field_name] = OrmFileField(
                model_name=model_name,
                name=field_name,
                pretty_name=field_name,
                django_field=field,
            )
        elif isinstance(field, type(None)):
            orm_field = _get_calculated_field(
                request, field_name, model_name, model, admin, model_fields
            )
            if orm_field:
                fields[orm_field.name] = orm_field
        else:
            field_type, choices = _get_field_type(model, field_name, field)

            rel_name = field_type.name
            if field_type is JSONType:
                json_fields = getattr(admin, "ddb_json_fields", {}).get(field_name)
                if json_fields:  # pragma: no branch
                    rel_name = f"{model_name}__{field_name}"
                    orm_models[rel_name] = _make_json_sub_module(
                        model_name, json_fields
                    )

            fields[field_name] = OrmConcreteField(
                model_name=model_name,
                name=field_name,
                pretty_name=field_name,
                type_=field_type,
                rel_name=rel_name,
                choices=choices,
            )
    orm_models[model_name] = OrmModel(fields=fields, admin=admin)
    return orm_models


def get_models(request):
    model_admins, admin_fields = _get_all_admin_fields(request)
    models = {}
    for model in admin_fields:
        models.update(
            _get_fields_for_model(request, model, model_admins[model], admin_fields)
        )
    types = {
        type_.name: OrmModel(get_fields_for_type(type_)) for type_ in TYPES.values()
    }

    return {**models, **types}
