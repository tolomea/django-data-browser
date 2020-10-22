from django.contrib.postgres.fields import ArrayField
from django.db import models


class ArrayModel(models.Model):  # pragma: postgres
    char_array_field = ArrayField(null=True, base_field=models.CharField(max_length=32))
    int_array_field = ArrayField(null=True, base_field=models.IntegerField())
    char_choice_array_field = ArrayField(
        null=True,
        base_field=models.CharField(max_length=32, choices=[("a", "A"), ("b", "B")]),
    )
    int_choice_array_field = ArrayField(
        null=True, base_field=models.IntegerField(choices=[(1, "A"), (2, "B")])
    )
