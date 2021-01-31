from dataclasses import dataclass
from typing import Sequence, Tuple

from django.db import models
from django.db.models import OuterRef, Subquery
from django.utils.html import format_html

from .types import (
    ASC,
    BaseType,
    BooleanType,
    DateTimeType,
    DateType,
    HTMLType,
    UnknownType,
)
from .util import annotation_path, s


@dataclass
class OrmBoundField:
    field: "OrmBaseField"
    previous: "OrmBoundField"
    full_path: Sequence[str]
    pretty_path: Sequence[str]
    queryset_path: Sequence[str]
    aggregate_clause: Tuple[str, models.Func] = None
    filter_: bool = False
    having: bool = False
    model_name: str = None

    @property
    def path_str(self):
        return s(self.full_path)

    @property
    def queryset_path_str(self):
        return s(self.queryset_path)

    @property
    def group_by(self):
        return self.field.can_pivot

    def _lineage(self):
        if self.previous:
            return self.previous._lineage() + [self]
        return [self]

    def annotate(self, request, qs):
        for field in self._lineage():
            qs = field._annotate(request, qs)
        return qs

    def _annotate(self, request, qs):
        return qs

    def __getattr__(self, name):
        return getattr(self.field, name)

    def parse_lookup(self, lookup, value):
        return self.type_.parse_lookup(lookup, value, self.choices)

    def format_lookup(self, lookup, value):
        return self.type_.format_lookup(lookup, value, self.choices)

    @classmethod
    def blank(cls):
        return cls(
            field=None, previous=None, full_path=[], pretty_path=[], queryset_path=[]
        )

    def get_format_hints(self, data):
        hints = self.type_.get_format_hints(self.path_str, data)
        return {**hints, **(self.format_hints or {})}


@dataclass
class OrmBaseField:
    model_name: str
    name: str
    pretty_name: str
    type_: BaseType = None
    concrete: bool = False
    rel_name: str = None
    can_pivot: bool = False
    choices: Sequence[Tuple[str, str]] = ()
    default_sort: str = None
    format_hints: dict = None
    actions: dict = None

    def __post_init__(self):
        if not self.type_:
            assert self.rel_name
        if self.concrete:
            assert self.type_
            # ideally all concrete fields would be equals filterable
            assert "equals" in self.type_.lookups or self.type_ in {
                UnknownType,
                HTMLType,
            }, (
                self.model_name,
                self.name,
                self.type_,
            )
        if self.can_pivot:
            assert self.type_

    def get_formatter(self):
        return self.type_.get_formatter(self.choices)


class OrmFkField(OrmBaseField):
    def __init__(self, model_name, name, pretty_name, rel_name):
        super().__init__(model_name, name, pretty_name, rel_name=rel_name)

    def bind(self, previous):
        previous = previous or OrmBoundField.blank()
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=previous.full_path + [self.name],
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=previous.queryset_path + [self.name],
        )


class OrmConcreteField(OrmBaseField):
    def __init__(
        self, model_name, name, pretty_name, type_, rel_name, choices, actions=None
    ):
        super().__init__(
            model_name,
            name,
            pretty_name,
            concrete=True,
            type_=type_,
            rel_name=rel_name,
            can_pivot=True,
            choices=choices or (),
            default_sort=ASC if type_ in [DateType, DateTimeType] else None,
            actions=actions,
        )

    def bind(self, previous):
        previous = previous or OrmBoundField.blank()
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=previous.full_path + [self.name],
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=previous.queryset_path + [self.name],
            filter_=True,
        )


class OrmRawField(OrmConcreteField):
    def bind(self, previous):
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=previous.full_path + [self.name],
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=previous.queryset_path,
            filter_=True,
        )


class OrmCalculatedField(OrmBaseField):
    def __init__(self, model_name, name, pretty_name, func):
        if getattr(func, "boolean", False):
            type_ = BooleanType
        else:
            type_ = HTMLType

        super().__init__(model_name, name, pretty_name, type_=type_, can_pivot=True)
        self.func = func

    def bind(self, previous):
        previous = previous or OrmBoundField.blank()
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=previous.full_path + [self.name],
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=previous.queryset_path + ["pk"],
            model_name=self.model_name,
        )

    def get_formatter(self):
        base_formatter = super().get_formatter()

        def format(obj):
            if obj is None:
                return None

            try:
                value = self.func(obj)
            except Exception as e:
                return str(e)

            return base_formatter(value)

        return format


class OrmBoundAnnotatedField(OrmBoundField):
    def _annotate(self, request, qs):
        from .orm_admin import admin_get_queryset

        return qs.annotate(
            **{
                s(self.queryset_path): Subquery(
                    admin_get_queryset(self.admin, request, [self.name])
                    .filter(pk=OuterRef(s(self.previous.queryset_path + ["pk"])))
                    .values(self.name)[:1],
                    output_field=self.django_field,
                )
            }
        )


class OrmAnnotatedField(OrmBaseField):
    def __init__(
        self, model_name, name, pretty_name, type_, django_field, admin, choices
    ):
        super().__init__(
            model_name,
            name,
            pretty_name,
            type_=type_,
            rel_name=type_.name,
            can_pivot=True,
            concrete=True,
            choices=choices or (),
        )
        self.django_field = django_field
        self.admin = admin

    def bind(self, previous):
        previous = previous or OrmBoundField.blank()

        full_path = previous.full_path + [self.name]
        return OrmBoundAnnotatedField(
            field=self,
            previous=previous,
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=annotation_path(full_path),
            filter_=True,
        )


class OrmFileField(OrmConcreteField):
    def __init__(self, model_name, name, pretty_name, django_field):
        super().__init__(
            model_name,
            name,
            pretty_name,
            type_=HTMLType,
            rel_name=HTMLType.name,
            choices=None,
        )
        self.django_field = django_field

    def get_formatter(self):
        def format(value):
            if not value:
                return value

            try:
                # some storage backends will hard fail if their underlying storage isn't
                # setup right https://github.com/tolomea/django-data-browser/issues/11
                return format_html(
                    '<a href="{}">{}</a>', self.django_field.storage.url(value), value
                )
            except Exception as e:
                return str(e)

        return format
