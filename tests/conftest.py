import dj_database_url
import django
import pytest
from django.conf import settings

DATABASE_CONFIG = dj_database_url.config(
    conn_max_age=600, default="sqlite:///db.sqlite3"
)

if DATABASE_CONFIG["ENGINE"] == "django.db.backends.postgresql":  # pragma: postgres
    JSON_FIELD_SUPPORT = django.VERSION > (2, 1)
else:
    JSON_FIELD_SUPPORT = django.VERSION > (3, 1)

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "tests.core",
    "data_browser",
]

if JSON_FIELD_SUPPORT:  # pragma: no branch
    INSTALLED_APPS.append("tests.json")

settings.configure(
    INSTALLED_APPS=INSTALLED_APPS,
    DATABASES={"default": DATABASE_CONFIG},
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
    MEDIA_URL="/media/",
    DATA_BROWSER_ALLOW_PUBLIC=True,
    USE_I18N=True,
    USE_TZ=True,
    TIME_ZONE="UTC",
)


@pytest.fixture
def req(rf, admin_user):
    req = rf.get("/")
    req.user = admin_user
    return req
