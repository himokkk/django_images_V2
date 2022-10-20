from django.urls import path

from .views import ImageCreateView, ImageListView, ImageUpdateView

urlpatterns = [
    path("image/list/", ImageListView.as_view()),
    path("image/create/", ImageCreateView.as_view()),
    path("image/update/<pk>", ImageUpdateView.as_view()),
]
