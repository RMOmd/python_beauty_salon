from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Master, Certificate, Portfolio, Service, Appointment, PortfolioImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'experience', 'is_available']
    list_filter = ['specialization', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'phone']

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['name', 'master', 'created_at']
    list_filter = ['master']
    search_fields = ['name', 'master__user__first_name', 'master__user__last_name']

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('master', 'created_at')
    list_filter = ('master', 'created_at')
    search_fields = ('master__user__first_name', 'master__user__last_name', 'description')

@admin.register(PortfolioImage)
class PortfolioImageAdmin(admin.ModelAdmin):
    list_display = ['master', 'created_at']
    list_filter = ['master']
    search_fields = ['master__user__first_name', 'master__user__last_name']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'master', 'service', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'master')
    search_fields = ('client__first_name', 'client__last_name', 'master__user__first_name', 'master__user__last_name')
    date_hierarchy = 'date'
