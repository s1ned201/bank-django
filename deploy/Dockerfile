FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install poetry

# Копирование файлов зависимостей
COPY ../pyproject.toml poetry.lock ./

# Установка зависимостей
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only main

# Копирование всего проекта
COPY .. .

COPY deploy/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Собираем статику
RUN python src/manage.py collectstatic --noinput

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]