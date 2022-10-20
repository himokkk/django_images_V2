from rest_framework.generics import ListAPIView

from ..serializers import ImageSerializer
from ..models import Image


class ImageListView(ListAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
