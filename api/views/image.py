import json
import os
from io import BytesIO

import requests
import validators
from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist
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
    def img_save(self, data, update=False, id=None):
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
        if isinstance(data["albumId"], str):
            try:
                data["albumId"] = int(data["albumId"])
            except UnidentifiedImageError:
                raise serializers.ValidationError("albbumId not a int")
        if "id" in data:
            data.pop("id")
        fields = [f.name for f in Image._meta.get_fields()]
        key_to_pop = []
        for key in data.keys():
            if key not in fields:
                key_to_pop.append(key)

        for key in key_to_pop:
            data.pop(key)

        serialized_data = ImageInputSerializer(data=data)
        serialized_data.is_valid(raise_exception=True)
        if not update:
            instance = Image.objects.create(**data)
        else:
            try:
                instance = Image.objects.get(id=id)
            except ObjectDoesNotExist:
                return Response("Cannot find instance for this pk", status=status.HTTP_404_NOT_FOUND)
            try:
                instance.__dict__.update(**data)
            except ValidationError:
                return Response("Cannot update instance", status=status.HTTP_400_BAD_REQUEST)

        file_name = str(instance.id) + "." + img.format.lower()
        path = os.path.join(settings.MEDIA_ROOT, "photos", file_name)
        img.save(path)
        instance.image = file_name
        instance.save()
        return Response(serialized_data.data)


class ImageCreateView(ImageSave, CreateAPIView):
    serializer_class = ImageInputSerializer
    queryset = Image.objects.all()

    def perform_create(self, serializer):
        data = self.request.data
        self.img_save(data)


class ImageUpdateView(ImageSave, UpdateAPIView):
    serializer_class = ImageInputSerializer
    queryset = Image.objects.all()
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        data = self.request.data
        id = kwargs.get("pk", None)
        if not id:
            raise Exception("Missing pk in URL")
        x = self.img_save(data, update=True, id=id)
        return x


class ImportImagesFromLink(ImageSave, APIView):
    def post(self, request):
        url = request.data.get("url", None)
        if not url:
            return Response("Wrong URL given", status=status.HTTP_400_BAD_REQUEST)
        if not validators.url(url):
            raise Response("URL not valid", status=status.HTTP_400_BAD_REQUEST)
        response = requests.get(url)
        content = json.loads(response.content)

        for element in content:
            self.img_save(data=element)
        return Response(status=status.HTTP_201_CREATED)


class ImportImagesFromFile(ImageSave, APIView):
    def post(self, request):
        file_obj = request.FILES.get("file", None)
        file_content = file_obj.file.read()
        if not file_obj:
            return Response("Wrong file given", status=status.HTTP_400_BAD_REQUEST)
        try:
            content = json.loads(file_content)
        except json.JSONDecodeError:
            return Response("Cannot convert file content to json", status=status.HTTP_400_BAD_REQUEST)

        for element in content:
            self.img_save(data=element)
        return Response(status=status.HTTP_201_CREATED)
