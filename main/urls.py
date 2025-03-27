from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('masters/', views.master_list, name='master_list'),
    path('masters/<int:pk>/', views.master_detail, name='master_detail'),
    path('appointment/create/', views.appointment_create, name='appointment_create'),
    path('appointment/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('profile/', views.profile, name='profile'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/add/<int:master_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:master_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('coupons/', views.coupons_view, name='coupons'),
    path('balance/', views.balance_view, name='balance'),
    path('balance/top-up/', views.balance_top_up, name='balance_top_up'),
    path('become-master/', views.become_master, name='become_master'),
    path('share/', views.share_view, name='share'),
    path('support/', views.support_view, name='support'),
    path('settings/', views.settings_view, name='settings'),
    path('pin-login/', views.pin_login, name='pin_login'),
    path('verify-biometric/', views.verify_biometric, name='verify_biometric'),
    path('masters/', views.masters, name='masters'),
    path('services/', views.services, name='services'),
    path('appointments/', views.appointments, name='appointments'),
    path('register/', views.register, name='register'),
    path('master/<int:master_id>/', views.master_detail, name='master_detail'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
] 