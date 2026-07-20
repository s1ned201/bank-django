from django.db import models
from django.conf import settings
from apps.core.domain.mixins import TimestampMixin

class ChatMessage(TimestampMixin):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chat_messages',
    )

    message = models.TextField(
        verbose_name='Сообщение пользователя',
    )

    response = models.TextField(
        verbose_name='Ответ ассистента',
    )

    class Meta:
        verbose_name = "Сообщение чата"
        verbose_name_plural = "Сообщения чата"
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user or "Аноним"}: {self.message[:50]}'