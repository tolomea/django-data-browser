from django.db.models import BooleanField


class AdminMixin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        for descriptor in getattr(self, "_DDB_annotations", {}).values():
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


class AnnotationDescriptor:
    def __init__(self, get_queryset):
        self.get_queryset = get_queryset

    def __set_name__(self, owner, name):
        self.name = name
        self.__name__ = name
        self.admin_order_field = name
        if not issubclass(owner, AdminMixin):  # pragma: no cover
            raise Exception(
                "Django Data Browser 'annotation' decorator used without 'AdminMixin'"
            )
        if not hasattr(owner, "_DDB_annotations"):  # pragma: no branch
            owner._DDB_annotations = {}
        owner._DDB_annotations[name] = self

    def __get__(self, instance, owner=None):
        return self

    def __call__(self, obj):  # pragma: no cover
        return getattr(obj, self.name)


annotation = AnnotationDescriptor
