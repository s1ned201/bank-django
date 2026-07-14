from django.conf import settings
from datetime import date, timedelta
from django.core.cache import cache
from apps.rates.models import ExchangeRate
from apps.core.domain.exceptions import NotFoundError

class ExchangeRateService:
    def _filter_allowed(self, rates_qs):
        """Фильтрует и оставляет только нужные нам валюты"""
        allowed = getattr(settings, 'ALLOWED_CURRENCY_CODES', [])
        if allowed:
            return rates_qs.filter(currency__code__in=allowed)
        return rates_qs

    def get_current_rates(self):
        """Возвращает словарь курсов валют"""
        data = cache.get('current_rates')
        if data:
            return data

        today = date.today()
        rates = ExchangeRate.objects.filter(date=today).select_related('currency')
        rates = self._filter_allowed(rates)

        if not rates.exists():
            last_rate = ExchangeRate.objects.order_by('-date').first()
            if not last_rate:
                raise NotFoundError("В базе нет курсов валют.")
            rates = ExchangeRate.objects.filter(date=last_rate.date).select_related('currency')
            rates = self._filter_allowed(rates)

        data = {}
        for r in rates:
            data[r.currency.code] = {
                'code': r.currency.code,
                'name': r.currency.name,
                'rate': str(r.rate),
                'date': str(r.date)
            }
        cache.set('current_rates', data, 3600)
        return data

    def get_history(self, currency_code: str, days: int = 7):
        allowed = getattr(settings, 'ALLOWED_CURRENCY_CODES', [])
        if allowed and currency_code.upper() not in allowed:
            raise NotFoundError(f"Валюта {currency_code} недоступна.")
        from_date = date.today() - timedelta(days=days)
        rates = ExchangeRate.objects.filter(
            currency__code=currency_code.upper(),
            date__gte=from_date
        ).order_by('date')
        if not rates:
            raise NotFoundError(f"Нет истории для {currency_code}")
        return [{'date': str(r.date), 'rate': str(r.rate)} for r in rates]