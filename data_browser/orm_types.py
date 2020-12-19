from django.db import models

from .common import debug_log
from .types import (
    BooleanType,
    DateTimeType,
    DateType,
    DurationType,
    JSONType,
    NumberArrayType,
    NumberChoiceArrayType,
    NumberChoiceType,
    NumberType,
    StringArrayType,
    StringChoiceArrayType,
    StringChoiceType,
    StringType,
    UnknownType,
    UUIDType,
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

_STRING_FIELDS = (
    models.CharField,
    models.TextField,
    models.GenericIPAddressField,
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
    models.UUIDField: UUIDType,
    **{f: StringType for f in _STRING_FIELDS},
    **{f: NumberType for f in _NUMBER_FIELDS},
}


def _fmt_choices(choices):
    return [(value, str(label)) for value, label in choices or []]


def get_field_type(field):
    if isinstance(field, ArrayField) and isinstance(
        field.base_field, _STRING_FIELDS
    ):  # pragma: postgres
        base_field, choices = get_field_type(field.base_field)
        array_types = {
            StringType: StringArrayType,
            NumberType: NumberArrayType,
            StringChoiceType: StringChoiceArrayType,
            NumberChoiceType: NumberChoiceArrayType,
        }
        if base_field in array_types:
            return array_types[base_field], choices
        else:
            debug_log(
                f"{field.model.__name__}.{field.name} unsupported subarray type {type(field.base_field).__name__}"
            )
            return UnknownType, None

    elif isinstance(field, ArrayField) and isinstance(
        field.base_field, _NUMBER_FIELDS
    ):  # pragma: postgres
        if field.base_field.choices:
            return NumberChoiceArrayType, _fmt_choices(field.base_field.choices)
        else:
            return NumberArrayType, None
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
                f"{field.model.__name__}.{field.name} unsupported type {type(field).__name__}"
            )
            res = UnknownType

    # Choice fields have different lookups
    if res is StringType and field.choices:
        return StringChoiceType, _fmt_choices(field.choices)
    elif res is NumberType and field.choices:
        return NumberChoiceType, _fmt_choices(field.choices)
    else:
        return res, None
