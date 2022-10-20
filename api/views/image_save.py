import os
from io import BytesIO

import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import URLValidator
from PIL import Image as Im
from PIL import UnidentifiedImageError
from rest_framework import serializers, status
from rest_framework.response import Response

from ..models import Image
from ..serializers import ImageInputSerializer


class ImageSave:
    def img_save(self, data, update=False, pk=None):
        url = data.get("url", None)
        validate_url = URLValidator()
        try:
            validate_url(url)
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
            except ValueError:
                raise serializers.ValueError("albumId not an int")
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
                instance = Image.objects.get(pk=pk)
            except ObjectDoesNotExist:
                return Response(
                    "Cannot find instance for this pk", status=status.HTTP_404_NOT_FOUND
                )
            try:
                instance.__dict__.update(**data)
            except ValidationError:
                return Response(
                    "Cannot update instance", status=status.HTTP_400_BAD_REQUEST
                )

        file_name = str(instance.id) + "." + img.format.lower()
        path = os.path.join(settings.MEDIA_ROOT, "photos", file_name)
        img.save(path)
        instance.image = file_name
        instance.save()
        return Response(serialized_data.data)
