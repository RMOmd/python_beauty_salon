# Салон красоты

Веб-приложение для салона красоты, разработанное на Django.

## Функциональность

- Авторизация и регистрация пользователей
- Просмотр услуг и мастеров
- Запись на процедуры
- Личный кабинет клиента
- Управление записями и заказами
- Избранные мастера
- Система бонусов и купонов

## Технологии

- Python 3.8+
- Django 5.0.2
- Bootstrap 5
- SQLite3
- django-allauth

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ваш-username/beauty-salon.git
cd beauty-salon
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env в корневой директории и добавьте необходимые переменные окружения:
```
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
```

5. Примените миграции:
```bash
python manage.py migrate
```

6. Запустите сервер разработки:
```bash
python manage.py runserver
```

## Структура проекта

- `beauty_salon/` - основные настройки проекта
- `main/` - основное приложение с бизнес-логикой
- `users/` - приложение для управления пользователями
- `static/` - статические файлы (CSS, JavaScript, изображения)
- `templates/` - HTML шаблоны
- `media/` - загружаемые пользователями файлы

## Лицензия

MIT 