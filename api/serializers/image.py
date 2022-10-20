from rest_framework import serializers

from ..models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "title", "album_id", "width", "height", "color", "image_url"]


class ImageInputSerializer(serializers.ModelSerializer):
    url = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = Image
        fields = ["title", "album_id", "color", "url"]
