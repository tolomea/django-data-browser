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
    MIDDLEWARE=[
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ],
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.template.context_processors.static",
                    "django.contrib.auth.context_processors.auth",
                ],
                "loaders": ["django.template.loaders.app_directories.Loader"],
            },
        }
    ],
    STATIC_URL="/static/",
)
