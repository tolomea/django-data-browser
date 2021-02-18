import json
import logging
from urllib.parse import urlencode

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import BooleanField
from django.urls import reverse


def attributes(**kwargs):
    def inner(func):
        for k, v in kwargs.items():
            setattr(func, k, v)
        return func

    return inner


class _Everything:
    def __contains__(self, item):
        return True


class _AdminOptions:
    ddb_ignore = False
    ddb_extra_fields = []
    ddb_hide_fields = []
    ddb_json_fields = {}
    ddb_default_filters = []
    ddb_action_url = None

    def get_ddb_ignore(self, request):
        return self.ddb_ignore

    def get_ddb_extra_fields(self, request):
        return list(self.ddb_extra_fields)

    def get_ddb_hide_fields(self, request):
        return list(self.ddb_hide_fields)

    def get_ddb_json_fields(self, request):
        return dict(self.ddb_json_fields)

    def get_ddb_default_filters(self):
        return list(self.ddb_default_filters)

    def get_ddb_action_url(self, request):
        if self.ddb_action_url:
            return self.ddb_action_url  # pragma: no cover

        meta = self.model._meta
        return reverse(f"admin:{meta.app_label}_{meta.model_name}_changelist") + "?"


def _get_option(admin, name, *args):
    field = f"ddb_{name}"
    func = f"get_ddb_{name}"

    if hasattr(admin, func):
        return getattr(admin, func)(*args)
    elif hasattr(admin, field):
        return getattr(admin, field)
    else:
        options = _AdminOptions()
        options.model = getattr(admin, "model", None)
        return getattr(options, func)(*args)


class _AdminAnnotations:
    def _get_fields_for_request(self, request):
        if hasattr(request, "data_browser"):
            return request.data_browser["fields"]
        elif (
            request.resolver_match
            and request.resolver_match.func.__name__ == "changelist_view"
        ):
            return set(self.get_list_display(request))
        else:
            return _Everything()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        fields = self._get_fields_for_request(request)

        for name, descriptor in self._ddb_annotations().items():
            if name not in fields:
                continue

            qs = descriptor.get_queryset(self, request, qs)

            annotation = qs.query.annotations.get(descriptor.name)
            if not annotation:  # pragma: no cover
                raise Exception(
                    f"Can't find annotation '{descriptor.name}' for {self}.{descriptor.name}"
                )

            field_type = getattr(annotation, "output_field", None)
            if not field_type:  # pragma: no cover
                raise Exception(
                    f"Annotation '{descriptor.name}' for {self}.{descriptor.name} doesn't specify 'output_field'"
                )

            descriptor.boolean = isinstance(field_type, BooleanField)
        return qs

    def get_readonly_fields(self, request, obj=None):
        res = super().get_readonly_fields(request, obj)
        return list(res) + list(self._ddb_annotations())

    @classmethod
    def _ddb_annotations(cls):
        res = {}
        for name in dir(cls):
            value = getattr(cls, name)
            if isinstance(value, _AnnotationDescriptor):
                res[name] = value
        return res


class AdminMixin(_AdminOptions, _AdminAnnotations):
    def changelist_view(self, request, extra_context=None):
        """ Inject ddb_url """
        extra_context = extra_context or {}

        if not self.get_ddb_ignore(request):
            url = reverse(
                "data_browser:query_html",
                args=[f"{self.model._meta.app_label}.{self.model.__name__}", ""],
            )
            args = self.get_ddb_default_filters()
            params = urlencode(
                [
                    (
                        f"{field}__{lookup}",
                        value
                        if isinstance(value, str)
                        else json.dumps(value, cls=DjangoJSONEncoder),
                    )
                    for field, lookup, value in args
                ]
            )
            extra_context["ddb_url"] = f"{url}?{params}"

        return super().changelist_view(request, extra_context)


class _AnnotationDescriptor:
    def __init__(self, get_queryset):
        self.get_queryset = get_queryset

    def __set_name__(self, owner, name):
        self.name = name
        self.__name__ = name
        self.admin_order_field = name

    def __get__(self, instance, owner=None):
        if not issubclass(owner, AdminMixin):  # pragma: no cover
            raise Exception(
                "Django Data Browser 'annotation' decorator used without 'AdminMixin'"
            )
        return self

    def __call__(self, obj):
        return getattr(obj, self.name)

    def __getattr__(self, name):
        return getattr(self.get_queryset, name)


def ddb_hide(func):  # pragma: no cover
    logging.getLogger(__name__).warning(
        "ddb_hide is deprecated in favor of @attributes(ddb_hide=True)"
    )
    func.ddb_hide = True
    return func


annotation = _AnnotationDescriptor
