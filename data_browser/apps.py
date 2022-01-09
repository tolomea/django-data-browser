from django.apps import AppConfig
from django.db.models import AutoField


class DataBrowserConfig(AppConfig):
    name = "data_browser"
    verbose_name = "Data Browser"
    default_auto_field = AutoField
