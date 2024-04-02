import json
from collections import defaultdict
from dataclasses import dataclass

from django import http
from django.apps import apps
from django.contrib.admin import site
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.admin.utils import model_format_dict
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import FieldDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.forms.models import _get_foreign_key
from django.urls import reverse
from django.utils.html import format_html

from data_browser.common import JsonResponse
from data_browser.common import debug_log
from data_browser.common import global_state
from data_browser.common import settings
from data_browser.helpers import AdminMixin
from data_browser.helpers import _AnnotationDescriptor
from data_browser.helpers import _get_option
from data_browser.helpers import attributes
from data_browser.orm_aggregates import get_aggregates_for_type
from data_browser.orm_debug import DebugQS
from data_browser.orm_fields import OrmAnnotatedField
from data_browser.orm_fields import OrmCalculatedField
from data_browser.orm_fields import OrmFileField
from data_browser.orm_fields import OrmFkField
from data_browser.orm_fields import OrmRawField
from data_browser.orm_fields import OrmRealField
from data_browser.orm_functions import get_functions_for_type
from data_browser.orm_types import get_field_type
from data_browser.types import TYPES
from data_browser.types import BooleanType
from data_browser.types import JSONType
from data_browser.types import NumberType
from data_browser.types import StringType
from data_browser.util import str_to_field
from data_browser.util import title_case


@dataclass
class OrmModel:
    full_name: str
    fields: dict
    admin: BaseModelAdmin = None
    pk: str = None
    verbose_name: str = None
    app_verbose_name: str = None

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

    def get_queryset(self, fields=(), debug=False):
        return admin_get_queryset(global_state.request, self.admin, fields, debug=debug)

    def get_http_request_for_action(self, action, pks):
        actions = admin_get_actions(global_state.request, self.admin)
        if action not in actions:
            raise http.Http404(f"'{action}' unknown action")  # pragma: no cover

        return JsonResponse({
            "method": "post",
            "url": _get_option(self.admin, "action_url", global_state.request),
            "data": [
                ("action", action),
                ("select_across", 0),
                ("index", 0),
                ("data_browser", 1),
                *[(ACTION_CHECKBOX_NAME, pk) for pk in pks],
            ],
        })


def get_model_name(model, sep="."):
    return f"{model._meta.app_label}{sep}{model.__name__}"


def get_model_verbose_name(model):
    return title_case(model._meta.verbose_name)


def get_app_verbose_name(model):
    app_config = apps.get_app_config(model._meta.app_label)
    return title_case(app_config.verbose_name)


def get_fields_for_type(type_):
    aggregates = get_aggregates_for_type(type_)
    functions = get_functions_for_type(type_)
    others = {}
    if type_.raw_type:
        others["raw"] = OrmRawField(
            type_.name, "raw", "raw", type_.raw_type, type_.raw_type.name, None
        )

    return {**aggregates, **functions, **others}


@attributes(short_description=settings.DATA_BROWSER_ADMIN_FIELD_NAME)
def open_in_admin(obj):
    if obj is None:  # pragma: no cover
        return None

    model_name = get_model_name(obj.__class__, "_")
    url_name = f"admin:{model_name}_change".lower()
    url = reverse(url_name, args=[obj.pk])
    return format_html('<a href="{}">{}</a>', url, obj)


def _admin_get_queryset(admin, request):
    # this is just a hook for tests to see the request
    return admin.get_queryset(request).using(settings.DATA_BROWSER_USING_DB)


def admin_get_queryset(request, admin, fields=(), debug=False):
    if debug:
        klass = admin.__class__
        return DebugQS(
            f"{klass.__module__}.{klass.__name__}(model,"
            " admin_site).get_queryset(request)"
        )
    else:
        orig = request.data_browser
        request.data_browser = {
            **request.data_browser,
            "calculated_fields": set(fields),
            "fields": set(fields),
        }
        try:
            return _admin_get_queryset(admin, request)
        finally:
            request.data_browser = orig


def admin_get_actions(request, admin):
    assert hasattr(request, "data_browser"), request

    res = {}
    for func, name, desc in admin.get_actions(request).values():
        if not getattr(func, "ddb_hide", False):
            desc %= model_format_dict(admin.opts)
            res[name] = func, desc
    return res


def _model_has_field(model, field_name):
    try:
        model._meta.get_field(field_name)
    except FieldDoesNotExist:
        return False
    return True


def _get_all_admin_fields(request):
    assert hasattr(request, "data_browser")

    def from_fieldsets(admin, include_calculated):
        auth_user_compat = settings.DATA_BROWSER_AUTH_USER_COMPAT
        if auth_user_compat and isinstance(admin, UserAdmin):
            obj = admin.model()  # get the change fieldsets, not the add ones
        else:
            obj = None

        fields = admin.get_fieldsets(request, obj)
        for f in flatten_fieldsets(fields):
            # skip calculated fields unless include_calculated given
            if include_calculated or _model_has_field(admin.model, f):
                yield f

    def visible(model_admin):
        if not request.user:
            return False  # pragma: no cover

        has_attrs = all(
            hasattr(model_admin, a) for a in ["get_fieldsets", "model", "get_queryset"]
        )
        if not has_attrs or not issubclass(model_admin.model, models.Model):
            debug_log(
                f"{type(model_admin)} instance does not look like a ModelAdmin or"
                " InlineModelAdmin"
            )
            return False

        if _get_option(model_admin, "ignore", request):
            return False

        return model_admin.has_view_permission(request)

    all_model_fields = defaultdict(set)
    hidden_model_fields = defaultdict(set)

    def get_common(admin, model):
        all_model_fields[model].update(from_fieldsets(admin, include_calculated=False))
        all_model_fields[model].update(_get_option(admin, "extra_fields", request))
        hidden_model_fields[model].update(_get_option(admin, "hide_fields", request))

    model_admins = {}
    admin_site = settings.DATA_BROWSER_ADMIN_SITE or site
    for model, model_admin in admin_site._registry.items():
        if visible(model_admin):
            model_admins[model] = model_admin
            all_model_fields[model].update(model_admin.get_list_display(request))
            all_model_fields[model].add(open_in_admin)
            get_common(model_admin, model)

            # check the inlines, these are already filtered for access
            for inline in model_admin.get_inline_instances(request):
                if visible(inline):
                    try:
                        fk_field = _get_foreign_key(model, inline.model, inline.fk_name)
                    except Exception as e:
                        debug_log(e)  # ignore things like GenericInlineModelAdmin
                    else:
                        if inline.model not in model_admins:  # pragma: no branch
                            model_admins[inline.model] = inline
                        all_model_fields[inline.model].add(fk_field.name)
                        get_common(inline, inline.model)

    for model, model_admin in model_admins.items():
        # add in the backside of related fields's
        for field_name in set(all_model_fields[model]):  # copy because we might modify
            if _model_has_field(model, field_name):
                field = model._meta.get_field(field_name)
                if (
                    field.is_relation
                    and field.related_model in all_model_fields
                    and not field.remote_field.hidden
                ):
                    all_model_fields[field.related_model].add(field.remote_field.name)

        # and the calculated fields
        all_model_fields[model].update(
            from_fieldsets(model_admin, include_calculated=True)
        )

        # and any annotations that weren't mentioned in field_sets etc
        if isinstance(model_admin, AdminMixin):
            all_model_fields[model].update(model_admin._ddb_annotations())

    # we always have the actual pk field and never have the "pk" proxy
    for model, fields in all_model_fields.items():
        fields.add(model._meta.pk.name)
        fields.discard("pk")
        fields.discard("__str__")

    # throw away the hidden ones
    for model, fields in hidden_model_fields.items():
        for f in fields:
            all_model_fields[model].discard(f)

    return model_admins, all_model_fields


def _make_verbose(name):
    return (name[0].upper() + name[1:]).replace("_", " ")


def _get_calculated_field(request, field_name, model_name, model, admin, model_fields):
    if isinstance(field_name, str):
        field_func = getattr(admin, field_name, None)
    else:
        # an actual function in list_display
        field_func = field_name
        field_name = str_to_field(
            getattr(field_func, "short_description", str(field_func.__name__))
        )

    if getattr(field_func, "ddb_hide", False):
        return None

    verbose_name = _make_verbose(
        getattr(field_func, "short_description", field_name.replace("_", " "))
    )

    if isinstance(field_func, _AnnotationDescriptor):
        qs = admin_get_queryset(request, admin, [field_name])

        annotation = qs.query.annotations.get(field_name)
        if not annotation:  # pragma: no cover
            raise Exception(
                f"Can't find annotation '{field_name}' for {admin}.{field_name}"
            )

        field = getattr(annotation, "output_field", None)
        if not field:  # pragma: no cover
            raise Exception(
                f"Annotation '{field_name}' for {admin}.{field_name} doesn't specify"
                " 'output_field'"
            )

        type_, choices = get_field_type(field_name, field)
        return OrmAnnotatedField(
            model_name=model_name,
            name=field_name,
            verbose_name=verbose_name,
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

        if field_func == open_in_admin and hasattr(admin, "get_actions"):
            actions = admin_get_actions(request, admin)
        else:
            actions = {}

        return OrmCalculatedField(
            model_name=model_name,
            name=field_name,
            verbose_name=verbose_name,
            func=field_func,
            actions=actions,
        )


def _make_json_sub_module(model_name, field_types):
    TYPE_MAP = {"string": StringType, "number": NumberType, "boolean": BooleanType}

    fields = dict(get_fields_for_type(JSONType))
    for field_name, type_name in field_types.items():
        type_ = TYPE_MAP[type_name]
        fields[field_name] = OrmRealField(
            model_name=model_name,
            name=field_name,
            verbose_name=field_name,
            type_=type_,
            rel_name=type_.name,
            choices=None,
        )

    return OrmModel(full_name=model_name, fields=fields)


def _get_fields_for_model(request, model, admin, admin_fields):
    fields = {}
    orm_models = {}

    model_name = get_model_name(model)
    model_fields = {f.name: f for f in model._meta.get_fields()}

    for field_name in admin_fields[model]:
        field = model_fields.get(field_name)
        verbose_name = (
            _make_verbose(getattr(field, "verbose_name", field_name)) if field else None
        )
        # FK's etc
        if isinstance(
            field, (models.ForeignKey, ForeignObjectRel, models.ManyToManyField)
        ):
            if isinstance(field, ForeignObjectRel):
                verbose_name = _make_verbose(field.get_accessor_name())

            if field.related_model in admin_fields:
                fields[field_name] = OrmFkField(
                    model_name=model_name,
                    name=field_name,
                    verbose_name=verbose_name,
                    rel_name=get_model_name(field.related_model),
                    to_many=field.one_to_many or field.many_to_many,
                )

            # if the related model is not exposed, and it's not a composite fk
            # then just expose it as it's native type
            else:
                foreign_related_fields = getattr(field, "foreign_related_fields", [])
                if len(foreign_related_fields) == 1:  # pragma: no branch
                    field_type, choices = get_field_type(
                        field_name, foreign_related_fields[0]
                    )
                    assert field_type != JSONType
                    fields[field_name] = OrmRealField(
                        model_name=model_name,
                        name=field_name,
                        verbose_name=verbose_name,
                        type_=field_type,
                        rel_name=field_type.name,
                        choices=choices,
                    )

        # Files and Images
        elif isinstance(field, models.FileField):
            fields[field_name] = OrmFileField(
                model_name=model_name,
                name=field_name,
                verbose_name=verbose_name,
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
            field_type, choices = get_field_type(field_name, field)

            rel_name = field_type.name
            if field_type is JSONType:
                json_fields = _get_option(admin, "json_fields", request).get(field_name)
                if json_fields:  # pragma: no branch
                    rel_name = f"{model_name}__{field_name}"
                    orm_models[rel_name] = _make_json_sub_module(rel_name, json_fields)
            if field_name == model._meta.pk.name and hasattr(admin, "get_actions"):
                actions = admin_get_actions(request, admin)
            else:
                actions = {}

            fields[field_name] = OrmRealField(
                model_name=model_name,
                name=field_name,
                verbose_name=verbose_name,
                type_=field_type,
                rel_name=rel_name,
                choices=choices,
                actions=actions,
            )

    orm_models[model_name] = OrmModel(
        full_name=model_name,
        fields=fields,
        admin=admin,
        pk=model._meta.pk.name,
        verbose_name=get_model_verbose_name(model),
        app_verbose_name=get_app_verbose_name(model),
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
        type_.name: OrmModel(full_name=type_.name, fields=get_fields_for_type(type_))
        for type_ in TYPES.values()
    }

    return {**models, **types}
