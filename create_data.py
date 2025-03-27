import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_salon.settings')
django.setup()

from main.models import Category, Master, Service
from django.contrib.auth.models import User

def create_test_data():
    # Очищаем существующие данные
    Service.objects.all().delete()
    Master.objects.all().delete()
    Category.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    
    # Создаем категории
    cat1 = Category.objects.create(
        name='Парикмахерские услуги',
        description='Стрижки, окрашивание, укладки',
        slug='hair-services'
    )
    cat2 = Category.objects.create(
        name='Ногтевой сервис',
        description='Маникюр, педикюр, наращивание',
        slug='nail-services'
    )
    cat3 = Category.objects.create(
        name='Макияж',
        description='Дневной и вечерний макияж',
        slug='makeup'
    )
    
    # Создаем пользователей и мастеров
    user1 = User.objects.create_user('anna', 'anna@example.com', 'anna12345', first_name='Анна', last_name='Иванова')
    Master.objects.create(
        user=user1,
        category=cat1,
        experience=5,
        description='Профессиональный стилист-парикмахер',
        phone='+7 (999) 123-45-67'
    )
    
    user2 = User.objects.create_user('maria', 'maria@example.com', 'maria12345', first_name='Мария', last_name='Петрова')
    Master.objects.create(
        user=user2,
        category=cat2,
        experience=3,
        description='Мастер ногтевого сервиса',
        phone='+7 (999) 234-56-78'
    )
    
    user3 = User.objects.create_user('elena', 'elena@example.com', 'elena12345', first_name='Елена', last_name='Сидорова')
    Master.objects.create(
        user=user3,
        category=cat3,
        experience=7,
        description='Визажист-стилист',
        phone='+7 (999) 345-67-89'
    )
    
    # Создаем услуги
    Service.objects.create(category=cat1, name='Женская стрижка', description='Модельная стрижка', price=2500, duration=60)
    Service.objects.create(category=cat1, name='Окрашивание', description='Окрашивание волос', price=4000, duration=120)
    
    Service.objects.create(category=cat2, name='Маникюр', description='Маникюр с покрытием', price=2000, duration=60)
    Service.objects.create(category=cat2, name='Педикюр', description='Педикюр с покрытием', price=2500, duration=90)
    
    Service.objects.create(category=cat3, name='Дневной макияж', description='Легкий макияж', price=2000, duration=40)
    Service.objects.create(category=cat3, name='Вечерний макияж', description='Вечерний образ', price=3000, duration=60)

if __name__ == '__main__':
    create_test_data()
    print('Тестовые данные успешно созданы!') 