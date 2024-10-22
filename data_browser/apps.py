from django.apps import AppConfig
from django.db.models import AutoField


class DataBrowserConfig(AppConfig):
    name = "data_browser"
    verbose_name = "Data Browser"
    default_auto_field = AutoField

    plugin_app = {
        'url_config': {
            'lms.djangoapp': {
                'namespace': '/admin/data-browser/',
                'regex': r'^data_browser/',
                'relative_path': 'urls',
            },
            'cms.djangoapp': {
                'namespace': '/admin/data-browser/',
                'regex': r'^data_browser/',
                'relative_path': 'urls',
            }
        },
    }

    def ready(self):
        from django.conf import settings
        if 'data_browser' not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS += ('data_browser',)
