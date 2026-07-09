from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from apps.core.domain.mixins import TimestampMixin, SoftDeleteMixin

class AuditLog(TimestampMixin, SoftDeleteMixin, models.Model):
    """
    Журнал событий
    """
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        verbose_name='Пользователь'
    )

    action = models.CharField(
        max_length=255,
        verbose_name='Действие'
    )

    ip_address = models.GenericIPAddressField(
        verbose_name='IP-адрес',
        null=True,
        blank=True
    )

    details = models.JSONField(
        verbose_name='Детали',
        default=dict,
        blank=True,
    )

    class Meta:
        verbose_name = "Запись аудита"
        verbose_name_plural = 'Записи аудита'
        ordering = ['-created_at']

    def __str__(self):
        user_str = self.user.username if self.user else 'Аноним'
        return f'{user_str} - {self.action} ({self.created_at:%Y-%m-%d %H:%M})'