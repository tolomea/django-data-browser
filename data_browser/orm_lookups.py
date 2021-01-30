from django.db.models import Q

from .types import IsNullType, StringType


def get_django_filter(field_type, path_str, lookup, filter_value):
    # because on JsonFields Q(field=None) != Q(field__isnull=True)
    if lookup == "is_null":
        if filter_value is True:
            return Q(**{path_str: None}) | Q(**{f"{path_str}__isnull": True})
        elif filter_value is False:
            return ~Q(**{path_str: None})
        else:
            assert False

    if field_type == IsNullType:
        assert lookup == "equals", lookup
        if filter_value is True:
            return Q(**{path_str: None}) | Q(**{path_str: True})
        elif filter_value is False:
            return Q(**{path_str: False})
        else:
            assert False

    if lookup == "field_equals":
        lookup, filter_value = filter_value
    elif field_type == StringType:
        lookup = {
            "equals": "iexact",
            "regex": "iregex",
            "contains": "icontains",
            "starts_with": "istartswith",
            "ends_with": "iendswith",
            "is_null": "isnull",
        }[lookup]
    elif lookup == "contains":  # pragma: postgres
        filter_value = [filter_value]
    else:
        lookup = {
            "equals": "exact",
            "is_null": "isnull",
            "gt": "gt",
            "gte": "gte",
            "lt": "lt",
            "lte": "lte",
            "contains": "contains",
            "length": "len",
            "has_key": "has_key",
        }[lookup]

    return Q(**{f"{path_str}__{lookup}": filter_value, f"{path_str}__isnull": False})
