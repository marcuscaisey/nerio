# Generated by Django 3.0.5 on 2020-04-22 17:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Url",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=120, unique=True)),
                ("target", models.TextField()),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_active", models.BooleanField(default=True)),
                ("visits", models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
