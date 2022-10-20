import json
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase

from .models import Image


class ImageAPIViewTest(APITestCase):
    def test_image_update(self):
        data = {
            "title": "title",
            "albumId": 1,
            "url": "https://media.geeksforgeeks.org/wp-content/uploads/20210318103632/gfg-300x300.png"
        }
        response = self.client.post("/api/image/create/", data, format='json')
        id = Image.objects.first().id
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        updated_data = {
            "title": "title1",
            "albumId": 12,
            "url": "https://scontent-vie1-1.xx.fbcdn.net/v/t1.6435-9/32498184_1757152210998322_30141221489868800_n.png?_nc_cat=102&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=zDqDUQH6hTcAX-Fxbn6&tn=Q_Px1EaULMYpz3Ok&_nc_ht=scontent-vie1-1.xx&oh=00_AT-Xmt04aUeiet9-r0o-guGaI2f-QzS9lewjkdq7O4kzQg&oe=6377CFEC"
        }
        response = self.client.patch("/api/image/update/"+str(id), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        instance = Image.objects.first()
        self.assertEqual(instance.title, updated_data.get("title"))
        self.assertEqual(instance.albumId, updated_data.get("albumId"))
        self.assertEqual(instance.color, updated_data.get("color"))
        self.assertEqual(instance.width, 2048)
        self.assertEqual(instance.height, 2048)

    def test_image_create(self):
        data = {
            "title": "title",
            "albumId": 1,
            "url": "https://media.geeksforgeeks.org/wp-content/uploads/20210318103632/gfg-300x300.png"
        }
        response = self.client.post("/api/image/create/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        instance = Image.objects.first()
        self.assertEqual(instance.title, data.get("title"))
        self.assertEqual(instance.albumId, data.get("albumId"))
        self.assertEqual(instance.color, data.get("color"))
        self.assertEqual(instance.width, 300)
        self.assertEqual(instance.height, 300)

        data["url"] = "12.png"
        response = self.client.post("/api/image/create/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data["url"] = "https://www.youtube.com/"
        response = self.client.post("/api/image/create/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_import_list_from_file(self):
        file = open("CLI/input.json")
        data = {
            "file": file
        }
        response = self.client.post("/api/image/import/file/", data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        file.close()

        file = open("CLI/input.json")
        instance = Image.objects.first()
        data = json.load(file)[0]
        self.assertEqual(instance.title, data.get("title"))
        self.assertEqual(instance.albumId, data.get("albumId"))
        self.assertEqual(instance.color, data.get("color"))
        self.assertEqual(instance.width, 300)
        self.assertEqual(instance.height, 300)

        file = open("CLI/invalid_input.json")
        data = {
            "file": file
        }
        response = self.client.post("/api/image/import/file/", data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        file.close()

        file = open("CLI/invalid_json_input.json")
        data = {
            "file": file
        }
        response = self.client.post("/api/image/import/file/", data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        file.close()

    def test_image_list_from_url(self):
        data = {
            "url": "https://jsonplaceholder.typicode.com/photos"
        }
        response = self.client.post("/api/image/create/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ImageModelTest(TestCase):
    def test_model(self):
        data = {
            "title": "title",
            "albumId": 1,
            "color": "123a",
            "height": 100,
            "width": 100,
            "image": "CLI/test_image.png"
        }
        instance = Image.objects.create(**data)
        self.assertEqual(instance.title, data.get("title"))
        self.assertEqual(instance.albumId, data.get("albumId"))
        self.assertEqual(instance.color, data.get("color"))
        self.assertEqual(instance.height, 100)
        self.assertEqual(instance.height, 100)

        data["color"] = "123x"
        with self.assertRaises(ValueError):
            Image.objects.create(**data)
