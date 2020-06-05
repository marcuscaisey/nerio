# Generated by Django 3.0.5 on 2020-06-04 16:28

from django.db import migrations, models

import core.validators


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_auto_20200603_1646"),
    ]

    operations = [
        migrations.AlterField(
            model_name="url",
            name="name",
            field=models.CharField(
                blank=True,
                error_messages={
                    "max_length": (
                        "Names must be no longer than %(limit_value)s characters."
                    ),
                    "unique": "This name has already been taken.",
                },
                help_text="This will be randomly generated, if left empty.",
                max_length=120,
                unique=True,
                validators=[
                    core.validators.URLNameCharacterValidator(),
                    core.validators.validate_url_name_doesnt_clash,
                ],
            ),
        ),
    ]
