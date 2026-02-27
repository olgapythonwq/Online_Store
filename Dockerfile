# Используем официальный образ python:3.12-slim
FROM python:3.13-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Отключаем venv у Poetry
ENV POETRY_VIRTUALENVS_CREATE=false POETRY_NO_INTERACTION=1 PYTHONUNBUFFERED=1

# Обновляем список пакетов и устанавливаем системные зависимости
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/\*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем только файлы зависимостей (Это важно для кеша)
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry install --no-root

# Копируем весь код проекта в контейнер
COPY . .

# Открываем порт 8000 для доступа к приложению
EXPOSE 8000

CMD ["sh", "-c", "python.manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
