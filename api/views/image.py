import json

import requests
import validators
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, UpdateAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Image
from ..serializers import ImageInputSerializer, ImageSerializer
from .image_save import ImageSave


class ImageListView(ListAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


class ImageDestroyView(DestroyAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    authentication_classes = []


class ImageCreateView(ImageSave, CreateAPIView):
    serializer_class = ImageInputSerializer
    queryset = Image.objects.all()

    def perform_create(self, serializer):
        data = self.request.data
        self.img_save(data)


class ImageUpdateView(ImageSave, UpdateAPIView):
    serializer_class = ImageInputSerializer
    queryset = Image.objects.all()
    http_method_names = ["patch"]

    def patch(self, request, *args, **kwargs):
        data = self.request.data
        pk = kwargs.get("pk", None)
        if not id:
            raise Exception("Missing pk in URL")
        return self.img_save(data, update=True, pk=pk)


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
            return Response(
                "Cannot convert file content to json",
                status=status.HTTP_400_BAD_REQUEST,
            )

        for element in content:
            self.img_save(data=element)
        return Response(status=status.HTTP_201_CREATED)
