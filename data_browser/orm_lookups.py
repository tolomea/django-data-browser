from .types import StringType


def get_django_lookup(field_type, lookup, filter_value):
    if lookup == "field_equals":
        lookup, filter_value = filter_value
        return lookup, filter_value
    elif field_type == StringType:
        return (
            {
                "equals": "iexact",
                "regex": "iregex",
                "contains": "icontains",
                "starts_with": "istartswith",
                "ends_with": "iendswith",
                "is_null": "isnull",
            }[lookup],
            filter_value,
        )
    else:
        return (
            {
                "equals": "exact",
                "is_null": "isnull",
                "gt": "gt",
                "gte": "gte",
                "lt": "lt",
                "lte": "lte",
                "contains": "contains",
                "length": "len",
                "has_key": "has_key",
            }[lookup],
            filter_value,
        )
