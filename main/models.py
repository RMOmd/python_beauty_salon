from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    name = models.CharField('Название категории', max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение категории', upload_to='categories/', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    about = models.TextField(blank=True)
    specialization = models.CharField(max_length=50, choices=[
        ('hair', 'Парикмахер'),
        ('nails', 'Мастер маникюра'),
        ('makeup', 'Визажист'),
        ('massage', 'Массажист'),
        ('cosmetology', 'Косметолог'),
        ('lashes', 'Лэшмейкер'),
        ('brows', 'Бровист'),
        ('permanent', 'Мастер перманентного макияжа'),
        ('epilation', 'Мастер эпиляции'),
    ], blank=True)
    experience = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    is_available = models.BooleanField(default=True)
    services = models.ManyToManyField('Service', related_name='masters', blank=True)

    def __str__(self):
        return self.user.get_full_name()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Автоматически добавляем услуги мастеру в зависимости от его специализации
        if self.specialization:
            category_map = {
                'hair': 'Волосы',
                'nails': 'Ногти',
                'makeup': 'Макияж',
                'massage': 'Массаж',
                'lashes': 'Ресницы',
                'brows': 'Брови',
                'permanent': 'Перманент',
                'epilation': 'Эпиляция',
            }
            if self.specialization in category_map:
                category_name = category_map[self.specialization]
                services = Service.objects.filter(category__name=category_name)
                self.services.set(services)

class Certificate(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='master_certificates')
    file = models.FileField(upload_to='certificates/', blank=True, null=True)
    name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.master}"

class Portfolio(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='portfolio_items')
    image = models.ImageField('Фото работы', upload_to='portfolio/')
    description = models.TextField('Описание работы')
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Портфолио'

    def __str__(self):
        return f"Работа мастера {self.master.user.get_full_name()}"

class Service(models.Model):
    name = models.CharField('Название услуги', max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    description = models.TextField('Описание услуги')
    price = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)
    duration = models.IntegerField('Длительность (минут)')
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return f"{self.name} - {self.category.name}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField('Примечания', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.client.get_full_name()} - {self.master.user.get_full_name()} - {self.date}"

class PortfolioImage(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='portfolio_images')
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Portfolio image for {self.master}"

class Favorite(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='favorites')
    master = models.ForeignKey('Master', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'master')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.master.user.get_full_name()}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('paid', 'Оплачен'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='orders')
    appointment = models.OneToOneField('Appointment', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} - {self.user.get_full_name()}"

class Coupon(models.Model):
    TYPE_CHOICES = [
        ('percent', 'Процент'),
        ('fixed', 'Фиксированная сумма'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='coupons')
    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.get_discount_type_display()}: {self.discount_value}"

    @property
    def is_valid(self):
        now = timezone.now()
        return self.valid_from <= now <= self.valid_to and not self.is_used

class ReferralCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referral_code')
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_referrals = models.PositiveIntegerField(default=0)
    total_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Реферальный код {self.code} - {self.user.get_full_name()}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        import string
        import random
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not ReferralCode.objects.filter(code=code).exists():
                return code

class ReferralInvitation(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_invitations')
    referred_email = models.EmailField()
    code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_registered = models.BooleanField(default=False)
    bonus_paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('referrer', 'referred_email')
        ordering = ['-created_at']

    def __str__(self):
        return f"Приглашение от {self.referrer.get_full_name()} для {self.referred_email}"

class UserPin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pin')
    pin_code = models.CharField('PIN-код', max_length=6)
    is_biometric_enabled = models.BooleanField('Биометрия включена', default=False)
    last_login = models.DateTimeField('Последний вход', auto_now=True)

    class Meta:
        verbose_name = 'PIN-код пользователя'
        verbose_name_plural = 'PIN-коды пользователей'

    def __str__(self):
        return f"PIN для {self.user.username}"

class Testimonial(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    text = models.TextField('Текст отзыва')
    rating = models.IntegerField('Оценка', choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.client.get_full_name()}"
