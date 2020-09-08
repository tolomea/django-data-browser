from django.db import models

try:
    from django.db.models import JSONField
except ImportError:  # pragma: django < 3.1
    from django.contrib.postgres.fields import JSONField


class JsonModel(models.Model):
    json_field = JSONField()
