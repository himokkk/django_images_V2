# Django Images App

Django Images App stores Photos from urls.

## Features
- Photos REST resource (list, create, update, delete) 
- Output fields (list): ID, title, album ID, width, height, color (dominant color), URL (URL to locally stored file)
- Input fields (create, update): title, album ID, URL
- Import photos from external API by URL; via both REST API and a CLI script
- Import photos from JSON file (expecting the same data format as the external API's); via both REST API and a CLI script
- Managing database from django-admin

## URLS
- Image List - api/image/list/
- Image Upload - api/image/create/
- Image Update - api/image/update/<id>
- Image Destroy - api/image/delete/<id>
- Image List imoport from URL - api/image/import/link/
- Image List imoport from JSON file - api/image/import/file/
- Admin - /admin/
- Photos - media/photos/<filename>

## Installation and Run

Requires [Python3.10](https://www.python.org/) and [docker-compose](https://docs.docker.com/compose/)  to run.

Installing with poetry.

```sh
poetry install
poetry run python manage.py migrate
```

Run with poetry

```sh
docker-compose up -d
poetry run python manage.py runserver
```

Installing with pip and virtualenv.

```sh
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
```

Run with pip

```sh
docker-compose up -d
python manage.py runserver
```
