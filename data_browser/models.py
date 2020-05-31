from __future__ import annotations

from django.conf import settings
from django.db import models
from django.http import QueryDict
from django.utils import crypto, timezone


def get_id():
    return crypto.get_random_string(length=12)


class View(models.Model):
    class Meta:
        permissions = [("make_view_public", "Can make a saved view publicly available")]

    id = models.CharField(primary_key=True, max_length=12, default=get_id)
    created_time = models.DateTimeField(default=timezone.now)

    name = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=True)
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    model_name = models.CharField(max_length=32, blank=False)
    fields = models.TextField(blank=True)
    query = models.TextField(blank=True)

    def get_query(self):
        from .query import Query

        return Query.from_request(self.model_name, self.fields, QueryDict(self.query))

    def __str__(self):
        return f"{self.model_name} view: {self.name}"
