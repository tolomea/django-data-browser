from django.contrib.postgres.fields import ArrayField
from django.db import models


class ArrayModel(models.Model):
    char_array_field = ArrayField(null=True, base_field=models.CharField(max_length=32))
    int_array_field = ArrayField(null=True, base_field=models.IntegerField())
    char_choice_array_field = ArrayField(
        null=True,
        base_field=models.CharField(
            max_length=32, choices=[("a", "A"), ("b", "B"), ("c", "C")]
        ),
    )
    int_choice_array_field = ArrayField(
        null=True,
        base_field=models.IntegerField(choices=[(1, "A"), (2, "B"), (3, "C")]),
    )
