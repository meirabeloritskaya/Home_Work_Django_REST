FROM python:3.12-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y libpq-dev build-essential

# Устанавливаем Poetrydocker-compose exec app bashpoetry show
RUN pip install poetry

# Устанавливаем рабочую директорию
WORKDIR /code

# Копируем файл pyproject.toml и poetry.lock (если есть)
COPY pyproject.toml poetry.lock* /code/

# Устанавливаем зависимости через Poetry
RUN poetry install --no-dev

# Копируем остальные файлы проекта
COPY . /code/

# Запуск приложения с использованием poetry run
CMD ["sh", "-c", "poetry run python manage.py migrate && poetry run python manage.py runserver 0.0.0.0:8000"]