# Foodgram - продуктовый помощник

Foodgram это web-сервис для поиска и публикации рецептов. Пользователям доступен просмотр и создание рецептов,
подписки на понравившихся авторов, а также добавление рецептов в список избранного с возможностью
выгрузки списка покупок в формате .txt.

## Данные для входа в админку

Почта: admin@example.com
Пароль: admin

## Стек технологий

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

## Как запустить проект на локальной машине

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/AxelVonReems/foodgram-project-react
```

Перейти в папку с проектом

```
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```
WIN: python -m venv venv
MAC: python3 -m venv venv
```

```
WIN: source venv/scripts/activate
MAC: source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
WIN: python -m pip install --upgrade pip
MAC: python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

В файле settings.py заменить базу данных с PostgreSQL на SQLite3 следуя подсказкам в самом файле.

Выполнить миграции:

```
WIN: python manage.py makemigrations  
MAC: python3 manage.py makemigrations
```

```
WIN: python manage.py migrate --noinput
MAC: python3 manage.py migrate --noinput
```

Запустить сервер:

```
WIN: python manage.py runserver
MAC: python3 manage.py runserver
```

Сервис будет доступен по адресу: http://127.0.0.1:8000/

## Как запустить проект с помощью Docker

Клонировать репозиторий и перейти в него в командной строке.

Перейти в папку с проектом

Cоздать и активировать виртуальное окружение

Установить зависимости из файла requirements.txt

В папке infra создать и заполнить по образцу .env-файл:

```
DB_ENGINE=django.db.backends.postgresql - указываем, что работаем с postgresql
DB_NAME=postgres - имя базы данных
POSTGRES_USER=postgres - логин для подключения к базе данных
POSTGRES_PASSWORD=postgres - пароль для подключения к БД
DB_HOST=db - название сервиса (контейнера)
DB_PORT=5432 - порт для подключения к БД 
SECRET_KEY=ХХХХХХХХХХХХХХХХХ - секретный ключ проекта Django
DEBUG='False' - настройка дебаггера
```

Собрать и запустить контейнер с помощью Docker-compose:

```
docker-compose build
docker-compose up
```

Выполнить миграции через Docker-compose:

```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate --noinput
```

Загрузить ингредиенты и теги:

```
docker-compose exec web python manage.py load_ingrs
docker-compose exec web python manage.py load_tags
```

Собрать статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```

Создать через Docker-compose суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

## Автор проекта

Алексей Смирнов. GitHub: https://github.com/AxelVonReems/
