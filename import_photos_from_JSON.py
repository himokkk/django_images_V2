import json
import os
import sys

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "images.settings")
django.setup()

from api.views.image import ImageSave


class ImportFromFile(ImageSave):
    def __init__(self, filename):
        with open(filename) as file:
            content = json.loads(file.read())
            for data in content:
                self.img_save(data=data)


filename = os.path.join("CLI", "input.json")
if len(sys.argv) > 1:
    filename = sys.argv[1]
instance = ImportFromFile(filename=filename)
