# Используем официальный образ nginx
FROM nginx:latest

# Создаём директорию для статических файлов
RUN mkdir -p /app/staticfiles

# Копируем файл конфигурации nginx в контейнер - есть в docker-compose
#COPY nginx.conf /etc/nginx/nginx.conf

# Открываем порт 80 для HTTP-трафика
EXPOSE 80
