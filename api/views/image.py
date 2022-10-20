import json
import os
from io import BytesIO

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from PIL import Image as Im
from PIL import UnidentifiedImageError
from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Image
from ..serializers import ImageInputSerializer, ImageSerializer


class ImageListView(ListAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


class ImageSave:
    def img_save(self, data):
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
        instance.image = file_name
        instance.save()

    def perform_create(self, serializer):
        data = self.request.data
        self.img_save(data)


class ImageCreateView(ImageSave, CreateAPIView):
    serializer_class = ImageInputSerializer
    queryset = Image.objects.all()


class ImageUpdateView(ImageSave, UpdateAPIView):
    serializer_class = ImageInputSerializer
    queryset = Image.objects.all()


class ImportImagesFromLink(ImageSave, APIView):
    def post(self, request):
        url = request.data.get("url", None)
        if not url:
            return Response("Wrong URL given", status=status.HTTP_400_BAD_REQUEST)
        response = requests.get(url)
        content = json.loads(response.content)

        for element in content:
            self.img_save(data=element)
        return Response(status=status.HTTP_201_CREATED)


class ImportImagesFromFile(ImageSave, APIView):
    def post(self, request):
        file_obj = request.FILES.get("file", None)
        if not file_obj:
            return Response("Wrong file given", status=status.HTTP_400_BAD_REQUEST)

        content = json.loads(file_obj.file.read())
        for element in content:
            self.img_save(data=element)
        return Response(status=status.HTTP_201_CREATED)
