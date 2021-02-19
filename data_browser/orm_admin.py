import json
from collections import defaultdict
from dataclasses import dataclass

from django import http
from django.contrib.admin import site
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.admin.utils import flatten_fieldsets, model_format_dict
from django.contrib.auth.admin import UserAdmin
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models.fields.reverse_related import ForeignObjectRel, OneToOneRel
from django.forms.models import _get_foreign_key
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify

from .common import JsonResponse, debug_log, settings
from .helpers import AdminMixin, _AnnotationDescriptor, _get_option, attributes
from .orm_aggregates import get_aggregates_for_type
from .orm_fields import (
    OrmAnnotatedField,
    OrmCalculatedField,
    OrmConcreteField,
    OrmFileField,
    OrmFkField,
    OrmRawField,
)
from .orm_functions import get_functions_for_type
from .orm_types import get_field_type
from .types import TYPES, BooleanType, JSONType, NumberType, StringType

OPEN_IN_ADMIN = "admin"


@dataclass
class OrmModel:
    fields: dict
    admin: BaseModelAdmin = None
    pk: str = None

    @property
    def root(self):
        return bool(self.admin)

    @property
    def default_filters(self):
        default_filters = _get_option(self.admin, "default_filters")
        assert isinstance(default_filters, list)
        return [
            (f, l, v if isinstance(v, str) else json.dumps(v, cls=DjangoJSONEncoder))
            for (f, l, v) in default_filters
        ]

    def get_queryset(self, request, fields=()):
        return admin_get_queryset(self.admin, request, fields)

    def get_action_request(self, request, action, pks):
        actions = admin_get_actions(self.admin, request)
        if action not in actions:
            raise http.Http404(f"'{action}' unknown action")  # pragma: no cover

        return JsonResponse(
            {
                "method": "post",
                "url": _get_option(self.admin, "action_url", request),
                "data": [
                    ("action", action),
                    ("select_across", 0),
                    ("index", 0),
                    ("data_browser", 1),
                    *[(ACTION_CHECKBOX_NAME, pk) for pk in pks],
                ],
            }
        )


def get_model_name(model, sep="."):
    return f"{model._meta.app_label}{sep}{model.__name__}"


def get_fields_for_type(type_):
    aggregates = get_aggregates_for_type(type_)
    functions = get_functions_for_type(type_)
    others = {}
    if type_.raw_type:
        others["raw"] = OrmRawField(
            type_.name, "raw", "raw", type_.raw_type, type_.raw_type.name, None
        )

    return {**aggregates, **functions, **others}


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


def admin_get_actions(admin, request):
    request.data_browser = {"calculated_fields": set(), "fields": set()}
    res = {}
    for func, name, desc in admin.get_actions(request).values():
        if not getattr(func, "ddb_hide", False):
            desc %= model_format_dict(admin.opts)
            res[name] = func, desc
    return res


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
            if all_ or hasattr(admin.model, f):
                yield f

    def visible(model_admin, request):
        has_attrs = all(
            hasattr(model_admin, a) for a in ["get_fieldsets", "model", "get_queryset"]
        )
        if not has_attrs or not issubclass(model_admin.model, models.Model):
            debug_log(
                f"{type(model_admin)} instance does not look like a ModelAdmin or InlineModelAdmin"
            )
            return False

        if _get_option(model_admin, "ignore", request):
            return False

        return model_admin.has_view_permission(request)

    all_admin_fields = defaultdict(set)
    hidden_fields = defaultdict(set)

    def get_common(admin, model):
        all_admin_fields[model].update(from_fieldsets(admin, False))
        all_admin_fields[model].update(_get_option(admin, "extra_fields", request))
        hidden_fields[model].update(_get_option(admin, "hide_fields", request))

    model_admins = {}
    for model, model_admin in site._registry.items():
        if visible(model_admin, request):
            model_admins[model] = model_admin
            all_admin_fields[model].update(model_admin.get_list_display(request))
            all_admin_fields[model].add(open_in_admin)
            get_common(model_admin, model)

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
                        all_admin_fields[inline.model].add(fk_field.name)
                        get_common(inline, inline.model)

    for model, model_admin in model_admins.items():
        if isinstance(model_admin, AdminMixin):
            all_admin_fields[model].update(model_admin._ddb_annotations())
        all_admin_fields[model].update(from_fieldsets(model_admin, True))

    # we always have the actual pk field and never have the "pk" proxy
    for model, fields in all_admin_fields.items():
        fields.add(model._meta.pk.name)
        fields.discard("pk")
        fields.discard("__str__")

    # throw away the hidden ones
    for model, fields in hidden_fields.items():
        for f in fields:
            all_admin_fields[model].discard(f)

    return model_admins, all_admin_fields


def _upper(name):
    return name[0].upper() + name[1:]


def _get_calculated_field(request, field_name, model_name, model, admin, model_fields):
    if isinstance(field_name, str):
        field_func = getattr(admin, field_name, None)
    else:
        # an actual function in list_display
        field_func = field_name
        field_name = slugify(
            getattr(field_func, "short_description", str(field_func.__name__))
        )

    if getattr(field_func, "ddb_hide", False):
        return None

    pretty_name = _upper(
        getattr(field_func, "short_description", field_name.replace("_", " "))
    )

    if isinstance(field_func, _AnnotationDescriptor):
        qs = admin_get_queryset(admin, request, [field_name])

        annotation = qs.query.annotations.get(field_name)
        if not annotation:  # pragma: no cover
            raise Exception(
                f"Can't find annotation '{field_name}' for {admin}.{field_name}"
            )

        field = getattr(annotation, "output_field", None)
        if not field:  # pragma: no cover
            raise Exception(
                f"Annotation '{field_name}' for {admin}.{field_name} doesn't specify 'output_field'"
            )

        type_, choices = get_field_type(field)
        return OrmAnnotatedField(
            model_name=model_name,
            name=field_name,
            pretty_name=pretty_name,
            type_=type_,
            django_field=field,
            admin=admin,
            choices=choices,
        )
    else:
        if field_func is None:

            def field_func(obj):
                value = getattr(obj, field_name)
                return value() if callable(value) else value

        return OrmCalculatedField(
            model_name=model_name,
            name=field_name,
            pretty_name=pretty_name,
            func=field_func,
        )


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
            choices=None,
        )

    return OrmModel(fields)


def _get_fields_for_model(request, model, admin, admin_fields):
    fields = {}
    orm_models = {}

    model_name = get_model_name(model)
    model_fields = {f.name: f for f in model._meta.get_fields()}

    for field_name in admin_fields[model]:
        field = model_fields.get(field_name)
        pretty_name = (
            _upper(getattr(field, "verbose_name", field_name)) if field else None
        )
        # FK's and OneToOne's
        if isinstance(field, (models.ForeignKey, OneToOneRel)):
            if field.related_model in admin_fields:
                fields[field_name] = OrmFkField(
                    model_name=model_name,
                    name=field_name,
                    pretty_name=pretty_name,
                    rel_name=get_model_name(field.related_model),
                )
            elif len(field.foreign_related_fields) == 1:  # pragma: no branch
                field_type, choices = get_field_type(field.foreign_related_fields[0])
                assert field_type != JSONType
                fields[field_name] = OrmConcreteField(
                    model_name=model_name,
                    name=field_name,
                    pretty_name=pretty_name,
                    type_=field_type,
                    rel_name=field_type.name,
                    choices=choices,
                )

        # ManyToMany
        elif isinstance(field, (ForeignObjectRel, models.ManyToManyField)):
            pass
        # Files and Images
        elif isinstance(field, models.FileField):
            fields[field_name] = OrmFileField(
                model_name=model_name,
                name=field_name,
                pretty_name=pretty_name,
                django_field=field,
            )
        # Calculated and annotated fields
        elif isinstance(field, type(None)):
            orm_field = _get_calculated_field(
                request, field_name, model_name, model, admin, model_fields
            )
            if orm_field:
                fields[orm_field.name] = orm_field
        # Normal fields
        else:
            field_type, choices = get_field_type(field)

            rel_name = field_type.name
            if field_type is JSONType:
                json_fields = _get_option(admin, "json_fields", request).get(field_name)
                if json_fields:  # pragma: no branch
                    rel_name = f"{model_name}__{field_name}"
                    orm_models[rel_name] = _make_json_sub_module(
                        model_name, json_fields
                    )

            if field_name == model._meta.pk.name and hasattr(admin, "get_actions"):
                actions = admin_get_actions(admin, request)
            else:
                actions = {}

            fields[field_name] = OrmConcreteField(
                model_name=model_name,
                name=field_name,
                pretty_name=pretty_name,
                type_=field_type,
                rel_name=rel_name,
                choices=choices,
                actions=actions,
            )
    orm_models[model_name] = OrmModel(
        fields=fields, admin=admin, pk=model._meta.pk.name
    )
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
