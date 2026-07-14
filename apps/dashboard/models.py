from django.db import models
from django.conf import settings
from apps.core.domain.mixins import TimestampMixin
from apps.rates.models import Currency

class Account(TimestampMixin):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts',
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name='accounts',
    )

    balance = models.DecimalField(
        verbose_name='Баланс',
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    name = models.CharField(
        verbose_name='Название счета',
        max_length=100,
        blank=True,
        default='Основной',
    )

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    def __str__(self):
        return f'{self.user.username} - {self.name} ({self.balance})'

class Transaction(TimestampMixin):
    from_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='outgoing_transactions',
    )

    to_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='incoming_transactions',
        null=True,
        blank=True,
    )

    amount = models.DecimalField(
        verbose_name= 'Сумма',
        max_digits=14,
        decimal_places=2,
    )

    description = models.CharField(
        verbose_name= 'Описание',
        max_length=255,
        blank=True,
    )

    transaction_type = models.CharField(
        verbose_name='Тип',
        max_length=20,
        choices=[
            ('transfer', 'Перевод'),
            ('deposit', 'Пополнение'),
            ('withdrawal', 'Снятие'),
        ]
    )

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

    def __str__(self):
        return (f"{self.transaction_type} {self.amount} {self.from_account.currency.code}"
                f" ({self.created_at:%Y-%m-%d %H:%M})")