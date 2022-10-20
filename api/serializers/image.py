from django.conf import settings
from rest_framework import serializers

from ..models import Image


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ["id", "title", "albumId", "width", "height", "color", "image_url"]

    def get_image_url(self, obj):
        if obj.image:
            return (
                settings.HOST
                + settings.MEDIA_URL
                + "photos/"
                + obj.image.url.split("/")[-1]
            )
        return ""


class ImageInputSerializer(serializers.ModelSerializer):
    url = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = Image
        fields = ["title", "albumId", "url"]
