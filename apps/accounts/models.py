from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from datetime import timedelta
from django.utils import timezone

from django.conf import settings


class User(AbstractUser):
    """
    UserCustomModel
    telegram_id - идентификатор Telegram для 2FA и уведомлений
    telegram_username - username в Telegram
    is_telegram_verified - подтверждён ли Telegram
    phone_number - номер телефона
    avatar - аватар пользователя
    is_manager - роль сотрудника банка
    """
    telegram_id = models.BigIntegerField(
        verbose_name="Telegram ID",
        null=True,
        blank=True,
        unique=True,
    )
    telegram_username = models.CharField(
        verbose_name="Telegram Username",
        max_length=150,
        null=True,
        blank=True,
    )
    is_telegram_verified = models.BooleanField(
        verbose_name="Telegram подтверждён",
        default=False,
    )
    phone_number = models.CharField(
        verbose_name="Номер телефона",
        max_length=20,
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="avatars/",
        null=True,
        blank=True,
    )
    telegram_avatar_url = models.URLField(
        verbose_name="URL аватарки Telegram",
        blank=True,
        null=True,
    )
    is_manager = models.BooleanField(
        verbose_name="Менеджер",
        default=False,
    )

    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="группы",
        blank=True,
        related_name="accounts_user_groups",
        related_query_name="accounts_user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="права",
        blank=True,
        related_name="accounts_user_permissions",
        related_query_name="accounts_user",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        db_table = "accounts_user"

    def __str__(self):
        return self.get_full_name() or self.username

class TwoFACode(models.Model):

    code = models.CharField(
        max_length=6,
        verbose_name="Код"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="twofa_codes",
        verbose_name="Пользователь"
    )

    expires_at = models.DateTimeField(
        verbose_name="Срок действия",
    )

    is_used = models.BooleanField(
        verbose_name="Использован",
        default=False,
    )

    ip_address = models.GenericIPAddressField(
        verbose_name="IP-адрес",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Код 2FA"
        verbose_name_plural = "Коды 2FA"

    def __str__(self):
        return f"{self.user.username} - {self.code}"

    @staticmethod
    def generate_code():
        """Генерация рандомного 6 значного кода"""
        return str(random.randint(100000, 999999))

    def is_expired(self):
        return timezone.now() > self.expires_at