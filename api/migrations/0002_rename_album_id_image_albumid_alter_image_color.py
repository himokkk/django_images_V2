# Generated by Django 4.1.2 on 2022-10-20 05:00

from django.db import migrations, models

import api.models.image


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="image",
            old_name="album_id",
            new_name="albumId",
        ),
        migrations.AlterField(
            model_name="image",
            name="color",
            field=models.CharField(
                blank=True,
                max_length=8,
                null=True,
                validators=[api.models.image.Image.hex_validator],
            ),
        ),
    ]
