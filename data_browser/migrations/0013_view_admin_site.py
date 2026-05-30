from django.db import migrations
from django.db import models


def populate_admin_site(apps, schema_editor):
    from data_browser.common import settings

    admin_site = settings.DATA_BROWSER_ADMIN_SITE
    View = apps.get_model("data_browser", "View")
    View.objects.update(admin_site=admin_site.name)


class Migration(migrations.Migration):
    dependencies = [("data_browser", "0012_can_share")]

    operations = [
        migrations.AddField(
            model_name="view",
            name="admin_site",
            field=models.CharField(default="admin", max_length=200),
        ),
        migrations.RunPython(populate_admin_site, migrations.RunPython.noop),
    ]
