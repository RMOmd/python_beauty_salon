from main.models import Category, Master, Service
from django.contrib.auth.models import User

# Создаем категории
categories = [
    Category.objects.create(name='Парикмахерские услуги', description='Стрижки, окрашивание, укладки'),
    Category.objects.create(name='Ногтевой сервис', description='Маникюр, педикюр, наращивание'),
    Category.objects.create(name='Макияж', description='Дневной и вечерний макияж, свадебный образ'),
    Category.objects.create(name='Массаж', description='Различные виды массажа'),
    Category.objects.create(name='Косметология', description='Уход за кожей, чистка, пилинг')
]

# Создаем пользователей для мастеров
users = [
    User.objects.create_user(username='anna', email='anna@example.com', password='password123', first_name='Анна', last_name='Иванова'),
    User.objects.create_user(username='maria', email='maria@example.com', password='password123', first_name='Мария', last_name='Петрова'),
    User.objects.create_user(username='elena', email='elena@example.com', password='password123', first_name='Елена', last_name='Сидорова'),
    User.objects.create_user(username='olga', email='olga@example.com', password='password123', first_name='Ольга', last_name='Козлова'),
    User.objects.create_user(username='natalia', email='natalia@example.com', password='password123', first_name='Наталья', last_name='Морозова')
]

# Создаем мастеров
masters = [
    Master.objects.create(
        user=users[0],
        category=categories[0],
        experience=5,
        description='Профессиональный стилист-парикмахер с опытом работы более 5 лет. Специализируется на сложных техниках окрашивания.',
        phone='+7 (999) 123-45-67'
    ),
    Master.objects.create(
        user=users[1],
        category=categories[1],
        experience=3,
        description='Мастер ногтевого сервиса. Владеет всеми современными техниками маникюра и дизайна ногтей.',
        phone='+7 (999) 234-56-78'
    ),
    Master.objects.create(
        user=users[2],
        category=categories[2],
        experience=7,
        description='Визажист-стилист. Создает неповторимые образы для любых мероприятий.',
        phone='+7 (999) 345-67-89'
    ),
    Master.objects.create(
        user=users[3],
        category=categories[3],
        experience=10,
        description='Профессиональный массажист с медицинским образованием. Владеет различными техниками массажа.',
        phone='+7 (999) 456-78-90'
    ),
    Master.objects.create(
        user=users[4],
        category=categories[4],
        experience=6,
        description='Косметолог-эстетист. Специализируется на уходовых процедурах и anti-age терапии.',
        phone='+7 (999) 567-89-01'
    )
]

# Создаем услуги для каждой категории
services = [
    # Парикмахерские услуги
    Service.objects.create(category=categories[0], name='Женская стрижка', description='Модельная стрижка любой сложности', price=2500, duration=60),
    Service.objects.create(category=categories[0], name='Окрашивание', description='Однотонное окрашивание', price=4000, duration=120),
    Service.objects.create(category=categories[0], name='Укладка', description='Укладка волос любой длины', price=1500, duration=40),
    
    # Ногтевой сервис
    Service.objects.create(category=categories[1], name='Маникюр', description='Классический маникюр с покрытием', price=2000, duration=60),
    Service.objects.create(category=categories[1], name='Педикюр', description='Классический педикюр с покрытием', price=2500, duration=90),
    
    # Макияж
    Service.objects.create(category=categories[2], name='Дневной макияж', description='Легкий дневной макияж', price=2000, duration=40),
    Service.objects.create(category=categories[2], name='Вечерний макияж', description='Яркий вечерний макияж', price=3000, duration=60),
    
    # Массаж
    Service.objects.create(category=categories[3], name='Классический массаж', description='Общий массаж тела', price=3000, duration=60),
    Service.objects.create(category=categories[3], name='Антицеллюлитный массаж', description='Массаж проблемных зон', price=2500, duration=45),
    
    # Косметология
    Service.objects.create(category=categories[4], name='Чистка лица', description='Механическая чистка лица', price=3500, duration=90),
    Service.objects.create(category=categories[4], name='Пилинг', description='Химический пилинг', price=4000, duration=45)
]

print('Данные успешно созданы!') 