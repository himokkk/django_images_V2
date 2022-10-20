from django.contrib import admin
from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=100)
    Image = models.ImageField(upload_to="photos")
    album_id = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    color = models.CharField(max_length=8, null=True, blank=True)
    image_url = models.TextField()


admin.site.register(Image)