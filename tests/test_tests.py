import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_update_test_migrations():
    # why does test.core even have migrations?
    # so the dependencies make sure that content types is migrated before test.core
    call_command("makemigrations", "--check")
