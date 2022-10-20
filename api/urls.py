from django.urls import path, include

from .views import ImageListView

urlpatterns = [
    path("x", ImageListView.as_view()),
]
