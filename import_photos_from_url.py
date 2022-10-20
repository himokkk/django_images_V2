import json
import os
import sys

import django
import requests
import validators

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "images.settings")
django.setup()

from api.views.image import ImageSave


class ImportFromFile(ImageSave):
    def __init__(self, url):
        if not url:
            raise ValueError("URL is null")
        if not validators.url(url):
            raise ValueError("URL not valid")
        response = requests.get(url)
        content = json.loads(response.content)
        for data in content:
            self.img_save(data=data)


url = "https://jsonplaceholder.typicode.com/photos"
if len(sys.argv) > 1:
    url = sys.argv[1]
instance = ImportFromFile(url=url)
