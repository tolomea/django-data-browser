from django.conf import settings

settings.configure(
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.staticfiles",
        "django.contrib.admin",
        "tests",
        "data_browser",
    ],
    DATABASES={
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}
    },
    ROOT_URLCONF="tests.urls",
)
