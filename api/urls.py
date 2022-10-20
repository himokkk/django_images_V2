from django.urls import path

from .views import (ImageCreateView, ImageListView, ImageUpdateView,
                    ImportImagesFromFile, ImportImagesFromLink)

urlpatterns = [
    path("image/list/", ImageListView.as_view()),
    path("image/create/", ImageCreateView.as_view()),
    path("image/update/<pk>", ImageUpdateView.as_view()),
    path("image/import/link/", ImportImagesFromLink.as_view()),
    path("image/import/file/", ImportImagesFromFile.as_view()),
]
