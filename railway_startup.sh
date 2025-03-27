#!/bin/bash

# Создаем директории для медиа-файлов
mkdir -p $RAILWAY_VOLUME_MOUNT/media

# Собираем статические файлы
python manage.py collectstatic --noinput

# Применяем миграции
python manage.py migrate

# Запускаем Gunicorn
gunicorn beauty_salon.wsgi:application --bind 0.0.0.0:$PORT 