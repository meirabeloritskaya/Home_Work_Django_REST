# Проект Home_Work_Django_REST

- веб-приложение, новый Django-проект.

## Описание:

Проект представляет собой Django REST API с использованием PostgreSQL для хранения данных, Redis для кэширования и Celery для обработки фоновых задач. Приложение разворачивается с помощью Docker и Docker Compose.
 

## Требования:


- Python 3.12
- Docker и Docker Compose (для развертывания с контейнерами)
- Poetry (для управления зависимостями внутри контейнера)

## Установка:

1. Клонируйте репозиторий:
```
git clone https://git@github.com:meirabeloritskaya/Home_Work_Django_REST.git
```
2. Установите зависимости:
```
poetry install
```
3. Соберите и запустите контейнеры с помощью Docker Compose:
```
docker-compose up -d --build
```
4. Примените миграции для базы данных:
```
docker-compose exec app poetry run python manage.py migrate
```
5. Запустите сервер Django:
```
docker-compose exec app poetry run python manage.py runserver 0.0.0.0:8000
```
6. Для запуска Celery Worker:
```
docker-compose exec celery poetry run celery -A config worker --loglevel=info
```

7. Для запуска Celery Beat (для планирования задач):
```
docker-compose exec celery-beat poetry run celery -A config beat --loglevel=info
```

## Документация:

Для получения дополнительной информации обратитесь к [документации](docs/README.md).

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE).
