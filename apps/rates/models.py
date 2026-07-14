from django.db import models
from apps.core.domain.mixins import TimestampMixin

class Currency(models.Model):
    code = models.CharField(verbose_name='Код', max_length=3, unique=True, db_index=True)
    name = models.CharField(verbose_name='Название', max_length=100)
    symbol = models.CharField(verbose_name='Символ', max_length=10, blank=True, default='')

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"

    def __str__(self):
        return f'{self.code}'

class ExchangeRate(TimestampMixin):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='rates')
    rate = models.DecimalField(verbose_name='Курс BYN за 1 единицу', max_digits=12, decimal_places=4)
    date = models.DateField(verbose_name='Дата', db_index=True)

    class Meta:
        verbose_name = "Курс валюты"
        verbose_name_plural = "Курсы валют"
        unique_together = ('currency', 'date')

    def __str__(self):
        return f"{self.currency.code} = {self.rate} на {self.date}"