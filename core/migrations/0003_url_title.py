# Generated by Django 3.0.5 on 2020-04-24 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_url_created_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="url",
            name="title",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
    ]