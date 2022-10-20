from io import BytesIO
import os

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from PIL import Image as Im
from PIL import UnidentifiedImageError
from rest_framework import serializers
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView

from ..models import Image
from ..serializers import ImageInputSerializer, ImageSerializer


class ImageListView(ListAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


class Image_save():
    def perform_create(self, serializer):
        data = self.request.data
        url = data.get("url", None)
        val = URLValidator()
        try:
            val(url)
        except ValidationError:
            raise serializers.ValidationError("not valid url")

        response = requests.get(url)
        if not response.ok:
            raise serializers.ValidationError("Cannot fetch data from URL")
        try:
            img = Im.open(BytesIO(response.content))
        except UnidentifiedImageError:
            raise serializers.ValidationError("Cannot import image")

        data["width"], data["height"] = img.size
        data.pop("url")
        ImageInputSerializer(data=data).is_valid(raise_exception=True)
        instance = Image.objects.create(**data)

        file_name = str(instance.id) + "." + img.format.lower()
        path = os.path.join(settings.MEDIA_ROOT, "photos", file_name)
        img.save(path)
        instance.Image = file_name
        instance.save()


class ImageCreateView(Image_save, CreateAPIView):
    serializer_class = ImageInputSerializer
    queryset = Image.objects.all()


class ImageUpdateView(Image_save, UpdateAPIView):
    serializer_class = ImageInputSerializer
    queryset = Image.objects.all()
