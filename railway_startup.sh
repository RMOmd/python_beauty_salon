#!/bin/sh

# Останавливаем выполнение при ошибках
set -e

echo "Starting deployment process..."

# Проверяем и создаем необходимые директории
echo "Setting up directories..."
DATA_DIR="${RAILWAY_VOLUME_MOUNT:-/data}"
MEDIA_DIR="$DATA_DIR/media"

mkdir -p "$MEDIA_DIR"
chmod -R 755 "$MEDIA_DIR"

# Проверяем переменные окружения
echo "Checking environment variables..."
if [ -z "$PORT" ]; then
    export PORT=8000
    echo "PORT not set, using default: 8000"
fi

# Собираем статические файлы
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Применяем миграции
echo "Applying database migrations..."
python manage.py migrate --noinput

# Запускаем Gunicorn напрямую
echo "Starting Gunicorn server..."
exec gunicorn beauty_salon.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --threads 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info 