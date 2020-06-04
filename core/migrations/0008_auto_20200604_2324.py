# Generated by Django 3.0.5 on 2020-06-04 23:24

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0007_auto_20200604_1628"),
    ]

    operations = [
        migrations.AlterField(
            model_name="url",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="created date"
            ),
        ),
        migrations.AlterField(
            model_name="url",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="urls",
                related_query_name="url",
                to=settings.AUTH_USER_MODEL,
                verbose_name="creator",
            ),
        ),
        migrations.AlterField(
            model_name="url",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="active"),
        ),
    ]
