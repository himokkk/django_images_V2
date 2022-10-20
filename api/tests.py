import json
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Image


class ImageTest(APITestCase):
    def test_image_update(self):
        data = {
            "title": "title",
            "albumId": 1,
            "color": "123",
            "url": "https://media.geeksforgeeks.org/wp-content/uploads/20210318103632/gfg-300x300.png"
        }
        response = self.client.post("/api/image/create/", data, format='json')
        id = Image.objects.first().id
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        updated_data = {
            "title": "title",
            "albumId": 12,
            "color": "1234",
            "url": "https://media.geeksforgeeks.org/wp-content/uploads/20210318103632/gfg-300x300.png"
        }
        response = self.client.patch("/api/image/update/"+str(id), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_image_create(self):
        data = {
            "title": "title",
            "albumId": 1,
            "color": "123",
            "url": "https://media.geeksforgeeks.org/wp-content/uploads/20210318103632/gfg-300x300.png"
        }
        response = self.client.post("/api/image/create/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


