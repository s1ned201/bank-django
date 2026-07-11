from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_telegram_verified',
    )
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'is_telegram_verified',
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'avatar')
        }),
        ('Telegram и 2FA', {
            'fields': ('telegram_id', 'telegram_username', 'is_telegram_verified')
        }),
        ('Права доступа', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'is_manager',
                'groups',
                'user_permissions',
            )
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'telegram_id',
                'telegram_username',
                'is_telegram_verified',
                'phone_number',
                'avatar',
                'is_manager',
            ),
        }),
    )