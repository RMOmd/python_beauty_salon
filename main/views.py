from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, Master, Service, Appointment, PortfolioImage, Certificate, Favorite, Order, Coupon, ReferralCode, ReferralInvitation, UserPin, Testimonial
from .forms import AppointmentForm
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import JsonResponse

def index(request):
    services = Service.objects.all()[:6]  # Получаем первые 6 услуг
    masters = Master.objects.all()[:6]    # Получаем первых 6 мастеров
    testimonials = Testimonial.objects.all()[:6]  # Получаем первые 6 отзывов
    
    context = {
        'services': services,
        'masters': masters,
        'testimonials': testimonials,
    }
    return render(request, 'main/index.html', context)

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'main/category_list.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'main/category_detail.html', {'category': category})

def master_list(request):
    masters = Master.objects.all()
    return render(request, 'main/master_list.html', {'masters': masters})

def master_detail(request, pk):
    master = get_object_or_404(Master, pk=pk)
    portfolio_items = master.portfolio_items.all()
    services = master.services.all()
    
    # Проверяем, есть ли мастер в избранном у текущего пользователя
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, master=master).exists()
    
    context = {
        'master': master,
        'portfolio_items': portfolio_items,
        'services': services,
        'is_favorite': is_favorite,
        'certificates': master.master_certificates.all(),
        'portfolio_images': master.portfolio_images.all()
    }
    return render(request, 'main/master_detail.html', context)

@login_required
def appointment_create(request):
    if request.method == 'POST':
        master_id = request.POST.get('master')
        service_id = request.POST.get('service')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        try:
            master = Master.objects.get(id=master_id)
            service = Service.objects.get(id=service_id)
            appointment_date = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            
            # Проверяем, не занято ли время
            if Appointment.objects.filter(
                master=master,
                date=appointment_date,
                status='confirmed'
            ).exists():
                messages.error(request, 'Это время уже занято. Пожалуйста, выберите другое время.')
                return redirect('main:appointment_create')
            
            # Создаем запись
            appointment = Appointment.objects.create(
                client=request.user,
                master=master,
                service=service,
                date=appointment_date,
                status='pending'
            )
            
            messages.success(request, 'Запись успешно создана! Ожидайте подтверждения от мастера.')
            return redirect('main:appointment_detail', pk=appointment.pk)
            
        except Master.DoesNotExist:
            messages.error(request, 'Выбранный мастер не найден.')
            return redirect('main:appointment_create')
        except Service.DoesNotExist:
            messages.error(request, 'Выбранная услуга не найдена.')
            return redirect('main:appointment_create')
        except ValueError as e:
            messages.error(request, f'Ошибка в формате даты или времени: {str(e)}')
            return redirect('main:appointment_create')
        except Exception as e:
            messages.error(request, f'Произошла ошибка при создании записи: {str(e)}')
            return redirect('main:appointment_create')
    
    masters = Master.objects.all()
    return render(request, 'main/appointment_create.html', {'masters': masters})

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, client=request.user)
    return render(request, 'main/appointment_detail.html', {'appointment': appointment})

@login_required
def profile(request):
    """Представление профиля пользователя"""
    appointments = Appointment.objects.filter(client=request.user).order_by('-date')
    context = {
        'user': request.user,
        'appointments': appointments
    }
    return render(request, 'main/profile.html', context)

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(client=request.user).order_by('-date')
    return render(request, 'main/appointment_list.html', {'appointments': appointments})

@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('master', 'master__user')
    return render(request, 'main/favorites.html', {'favorites': favorites})

@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).select_related(
        'appointment', 'appointment__service', 'appointment__master', 'appointment__master__user'
    )
    return render(request, 'main/orders.html', {'orders': orders})

@login_required
def coupons_view(request):
    coupons = Coupon.objects.filter(user=request.user)
    return render(request, 'main/coupons.html', {'coupons': coupons})

@login_required
def balance_view(request):
    return render(request, 'main/balance.html')

@login_required
def become_master_view(request):
    return render(request, 'main/become_master.html')

@login_required
def register_with_referral(request):
    ref_code = request.GET.get('ref')
    if ref_code:
        try:
            referral_code = ReferralCode.objects.get(code=ref_code)
            # Сохраняем реферальный код в сессии
            request.session['referral_code'] = ref_code
        except ReferralCode.DoesNotExist:
            messages.error(request, _('Неверный реферальный код'))
            return redirect('account_signup')
    return redirect('account_signup')

@login_required
def share_view(request):
    # Получаем или создаем реферальный код для пользователя
    referral_code, created = ReferralCode.objects.get_or_create(user=request.user)
    
    # Получаем статистику приглашений
    invitations = ReferralInvitation.objects.filter(referrer=request.user)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Проверяем, не зарегистрирован ли уже этот email
            if User.objects.filter(email=email).exists():
                messages.error(request, _('Этот email уже зарегистрирован в системе'))
            else:
                # Создаем приглашение
                invitation, created = ReferralInvitation.objects.get_or_create(
                    referrer=request.user,
                    referred_email=email,
                    defaults={'code': referral_code.code}
                )
                if created:
                    # Отправляем email с приглашением
                    # TODO: Реализовать отправку email
                    messages.success(request, _('Приглашение успешно отправлено'))
                else:
                    messages.info(request, _('Приглашение для этого email уже существует'))
    
    context = {
        'referral_code': referral_code,
        'invitations': invitations,
        'total_bonus': referral_code.total_bonus,
        'bonus_per_referral': 500,  # Фиксированный бонус за реферала
        'site_url': request.build_absolute_uri('/')[:-1]  # URL сайта без слеша в конце
    }
    
    return render(request, 'main/share.html', context)

@login_required
def support_view(request):
    return render(request, 'main/support.html')

@login_required
def settings_view(request):
    user_pin = None
    try:
        user_pin = request.user.pin
    except UserPin.DoesNotExist:
        pass

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'set_pin':
            pin_code = request.POST.get('pin_code')
            if pin_code and len(pin_code) == 4 and pin_code.isdigit():
                UserPin.objects.update_or_create(
                    user=request.user,
                    defaults={'pin_code': pin_code}
                )
                messages.success(request, 'PIN-код успешно установлен')
            else:
                messages.error(request, 'PIN-код должен состоять из 4 цифр')
        
        elif action == 'remove_pin':
            if user_pin:
                user_pin.delete()
                messages.success(request, 'PIN-код успешно удален')
        
        elif action == 'toggle_biometric':
            if user_pin:
                user_pin.is_biometric_enabled = not user_pin.is_biometric_enabled
                user_pin.save()
                status = 'включена' if user_pin.is_biometric_enabled else 'отключена'
                messages.success(request, f'Биометрическая аутентификация {status}')
        
        return redirect('main:settings')

    return render(request, 'main/settings.html', {
        'user_pin': user_pin
    })

@login_required
def become_master(request):
    # Проверяем, не является ли пользователь уже мастером
    if hasattr(request.user, 'master'):
        messages.warning(request, _('Вы уже являетесь мастером.'))
        return redirect('profile')
        
    if request.method == 'POST':
        try:
            # Создаем профиль мастера
            master_profile = Master.objects.create(
                user=request.user,
                phone=request.POST.get('phone'),
                specialization=request.POST.get('specialization'),
                experience=request.POST.get('experience'),
                about=request.POST.get('about')
            )
            
            # Обновляем личную информацию пользователя
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.save()
            
            # Обработка загруженных файлов портфолио
            portfolio_images = request.FILES.getlist('portfolio')
            for image in portfolio_images[:5]:  # Ограничиваем до 5 фотографий
                PortfolioImage.objects.create(
                    master=master_profile,
                    image=image
                )
            
            # Обработка сертификатов
            certificates = request.FILES.getlist('certificates')
            for cert in certificates:
                Certificate.objects.create(
                    master=master_profile,
                    file=cert,
                    name=cert.name
                )
            
            messages.success(request, _('Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.'))
            return redirect('profile')
            
        except Exception as e:
            messages.error(request, _('Произошла ошибка при отправке заявки. Пожалуйста, попробуйте снова.'))
            return redirect('become_master')
    
    return render(request, 'main/become_master.html')

@login_required
def balance_top_up(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = float(amount)
            if amount < 100:
                messages.error(request, _('Минимальная сумма пополнения 100 рублей'))
                return redirect('main:balance')
            
            # Здесь должна быть интеграция с платежной системой
            # В демо-версии просто добавляем сумму к балансу
            request.user.balance += amount
            request.user.save()
            
            messages.success(request, _('Баланс успешно пополнен'))
            return redirect('main:balance')
            
        except ValueError:
            messages.error(request, _('Неверная сумма'))
            return redirect('main:balance')
    
    return redirect('main:balance')

@login_required
def add_to_favorites(request, master_id):
    master = get_object_or_404(Master, id=master_id)
    Favorite.objects.get_or_create(user=request.user, master=master)
    messages.success(request, _('Мастер добавлен в избранное'))
    return redirect('main:master_detail', pk=master_id)

@login_required
def remove_from_favorites(request, master_id):
    master = get_object_or_404(Master, id=master_id)
    Favorite.objects.filter(user=request.user, master=master).delete()
    messages.success(request, _('Мастер удален из избранного'))
    return redirect('main:favorites')

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        
        # Отменяем связанную запись
        appointment = order.appointment
        appointment.status = 'cancelled'
        appointment.save()
        
        messages.success(request, _('Заказ успешно отменен'))
    else:
        messages.error(request, _('Невозможно отменить этот заказ'))
    return redirect('main:orders')

def pin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pin_code = request.POST.get('pin_code')
        
        try:
            user = User.objects.get(username=username)
            user_pin = UserPin.objects.get(user=user, pin_code=pin_code)
            
            login(request, user)
            return JsonResponse({'status': 'success', 'redirect_url': '/'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Пользователь не найден'})
        except UserPin.DoesNotExist:
            return JsonResponse({
                'status': 'error', 
                'message': 'PIN-код не установлен. Пожалуйста, войдите обычным способом и установите PIN-код в настройках.'
            })
    
    return render(request, 'main/pin_login.html')

def verify_biometric(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        biometric_data = request.POST.get('biometric_data')
        
        try:
            user = User.objects.get(username=username)
            user_pin = UserPin.objects.get(user=user, is_biometric_enabled=True)
            
            # Здесь будет проверка биометрических данных
            # В реальном приложении нужно использовать WebAuthn или другой протокол
            
            login(request, user)
            return JsonResponse({'status': 'success', 'redirect_url': '/'})
        except (User.DoesNotExist, UserPin.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Пользователь не найден или биометрия не включена'})
    
    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'})

def masters(request):
    masters_list = Master.objects.all()
    return render(request, 'main/masters.html', {'masters': masters_list})

def services(request):
    services_list = Service.objects.all()
    return render(request, 'main/services.html', {'services': services_list})

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'main/service_detail.html', {'service': service})

@login_required
def appointments(request):
    user_appointments = Appointment.objects.filter(client=request.user)
    return render(request, 'main/appointments.html', {'appointments': user_appointments})

@login_required
def favorites(request):
    return render(request, 'main/favorites.html')

@login_required
def orders(request):
    return render(request, 'main/orders.html')

def register(request):
    if request.method == 'POST':
        # Здесь будет логика регистрации
        pass
    return render(request, 'main/register.html')
