from django.contrib import admin
from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="photos", null=True, blank=True)
    albumId = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()

    def hex_validator(data):
        try:
            int(data, 16)
        except ValueError:
            raise ValueError("color must be hex")

    color = models.CharField(
        max_length=8, null=True, blank=True, validators=[hex_validator]
    )


admin.site.register(Image)
