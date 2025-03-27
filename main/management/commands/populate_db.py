from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Category, Service, Master, PortfolioImage
from django.core.files import File
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Populate database with initial data'

    def handle(self, *args, **kwargs):
        # Создаем категории
        categories = {
            'lashes': Category.objects.create(name='Ресницы', slug='lashes'),
            'hair': Category.objects.create(name='Волосы', slug='hair'),
            'nails': Category.objects.create(name='Ногти', slug='nails'),
            'makeup': Category.objects.create(name='Макияж', slug='makeup'),
            'permanent': Category.objects.create(name='Перманент', slug='permanent'),
            'brows': Category.objects.create(name='Брови', slug='brows'),
            'massage': Category.objects.create(name='Массаж', slug='massage'),
            'epilation': Category.objects.create(name='Эпиляция', slug='epilation')
        }

        # Создаем услуги
        services = {
            'lashes': [
                Service.objects.create(
                    category=categories['lashes'],
                    name='Наращивание ресниц (классика)',
                    description='Классическое наращивание ресниц',
                    price=2000,
                    duration=120
                ),
                Service.objects.create(
                    category=categories['lashes'],
                    name='Наращивание ресниц 2D',
                    description='Объемное наращивание ресниц',
                    price=2500,
                    duration=150
                )
            ],
            'hair': [
                Service.objects.create(
                    category=categories['hair'],
                    name='Женская стрижка',
                    description='Стрижка любой сложности',
                    price=1500,
                    duration=60
                ),
                Service.objects.create(
                    category=categories['hair'],
                    name='Окрашивание волос',
                    description='Окрашивание волос любой сложности',
                    price=3000,
                    duration=180
                )
            ],
            'nails': [
                Service.objects.create(
                    category=categories['nails'],
                    name='Маникюр',
                    description='Классический маникюр',
                    price=1000,
                    duration=60
                ),
                Service.objects.create(
                    category=categories['nails'],
                    name='Педикюр',
                    description='Классический педикюр',
                    price=1500,
                    duration=90
                )
            ],
            'makeup': [
                Service.objects.create(
                    category=categories['makeup'],
                    name='Дневной макияж',
                    description='Легкий дневной макияж',
                    price=2000,
                    duration=60
                ),
                Service.objects.create(
                    category=categories['makeup'],
                    name='Вечерний макияж',
                    description='Вечерний макияж любой сложности',
                    price=3000,
                    duration=90
                )
            ],
            'massage': [
                Service.objects.create(
                    category=categories['massage'],
                    name='Релакс-массаж',
                    description='Расслабляющий массаж всего тела',
                    price=2500,
                    duration=60
                )
            ],
            'epilation': [
                Service.objects.create(
                    category=categories['epilation'],
                    name='Восковая эпиляция ног',
                    description='Эпиляция ног горячим воском',
                    price=1500,
                    duration=60
                ),
                Service.objects.create(
                    category=categories['epilation'],
                    name='Восковая эпиляция рук',
                    description='Эпиляция рук горячим воском',
                    price=800,
                    duration=30
                ),
                Service.objects.create(
                    category=categories['epilation'],
                    name='Лазерная эпиляция',
                    description='Лазерная эпиляция любой зоны',
                    price=3000,
                    duration=60
                )
            ]
        }

        # Создаем мастеров
        masters_data = [
            {
                'username': 'anna',
                'first_name': 'Анна',
                'last_name': 'Иванова',
                'specialization': 'lashes',
                'experience': 3,
                'about': 'Профессиональный лэшмейкер'
            },
            {
                'username': 'elena',
                'first_name': 'Елена',
                'last_name': 'Петрова',
                'specialization': 'hair',
                'experience': 5,
                'about': 'Стилист-парикмахер'
            },
            {
                'username': 'maria',
                'first_name': 'Мария',
                'last_name': 'Сидорова',
                'specialization': 'nails',
                'experience': 4,
                'about': 'Мастер ногтевого сервиса'
            },
            {
                'username': 'olga',
                'first_name': 'Ольга',
                'last_name': 'Козлова',
                'specialization': 'makeup',
                'experience': 6,
                'about': 'Визажист'
            },
            {
                'username': 'natalia',
                'first_name': 'Наталья',
                'last_name': 'Морозова',
                'specialization': 'massage',
                'experience': 8,
                'about': 'Массажист'
            },
            {
                'username': 'tatiana',
                'first_name': 'Татьяна',
                'last_name': 'Соколова',
                'specialization': 'epilation',
                'experience': 4,
                'about': 'Специалист по эпиляции'
            },
            {
                'username': 'irina',
                'first_name': 'Ирина',
                'last_name': 'Волкова',
                'specialization': 'hair',
                'experience': 7,
                'about': 'Парикмахер-стилист'
            },
            {
                'username': 'svetlana',
                'first_name': 'Светлана',
                'last_name': 'Кузнецова',
                'specialization': 'makeup',
                'experience': 5,
                'about': 'Визажист-стилист'
            }
        ]

        for master_data in masters_data:
            # Создаем пользователя
            user = User.objects.create_user(
                username=master_data['username'],
                password='password123',
                first_name=master_data['first_name'],
                last_name=master_data['last_name']
            )

            # Создаем профиль мастера
            master = Master.objects.create(
                user=user,
                phone='+7(999)999-99-99',
                specialization=master_data['specialization'],
                experience=master_data['experience'],
                about=master_data['about']
            )

            # Связываем мастера с соответствующими услугами
            if master_data['specialization'] in services:
                master.services.set(services[master_data['specialization']])

        self.stdout.write(self.style.SUCCESS('Successfully created categories, services and masters')) 