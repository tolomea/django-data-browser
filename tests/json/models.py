from django.db import models


class JsonModel(models.Model):
    json_field = models.JSONField()
