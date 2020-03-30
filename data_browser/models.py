import json

from django.conf import settings
from django.db import models
from django.utils import timezone


class View(models.Model):
    created_time = models.DateTimeField(default=timezone.now)

    name = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=True)
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    app = models.CharField(max_length=16, blank=False)
    model = models.CharField(max_length=32, blank=False)
    fields = models.TextField(blank=True)
    query = models.TextField(blank=False)

    def get_query(self, media):
        from .query import Query

        return Query.from_request(
            self.app, self.model, self.fields, media, json.loads(self.query)
        )

    def __str__(self):
        return f"{self.model} view: {self.name}"
