# Generated by Django 3.2.18 on 2023-04-16 11:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("data_browser", "0010_shared")]

    operations = [
        migrations.AddField(
            model_name="view",
            name="folder",
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name="view", name="model_name", field=models.CharField(max_length=64)
        ),
    ]
