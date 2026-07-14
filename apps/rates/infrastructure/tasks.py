import logging
import xml.etree.ElementTree as ET
from datetime import datetime, date, timedelta
import requests
from celery import shared_task
from django.core.cache import cache
from apps.rates.models import Currency, ExchangeRate

logger = logging.getLogger(__name__)
NBRB_URL = "https://www.nbrb.by/Services/XmlExRates.aspx"

@shared_task
def update_exchange_rates():
    """Загружает и сохраняет курс с API НацБанка"""
    today = date.today()
    url = f"{NBRB_URL}?ondate={today.strftime('%m/%d/%Y')}"

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Не удалось получить XML от НБ РБ: {e}")
        return

    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as e:
        logger.error(f"Ошибка парсинга XML: {e}")
        return

    added = updated = 0

    for valute in root.findall('Currency'):
        char_code = valute.find('CharCode').text
        name = valute.find('Name').text
        scale = int(valute.find('Scale').text)
        rate_str = valute.find('Rate').text
        rate = float(rate_str) / scale

        currency, created = Currency.objects.update_or_create(code=char_code, defaults={'name': name})
        if created:
            added += 1
        _, created = ExchangeRate.objects.update_or_create(
            currency=currency, date=today, defaults={'rate': rate}
        )
        if created:
            updated += 1

    logger.info(f"Курсы НБ РБ обновлены: валют добавлено {added}, курсов {updated}")
    cache.delete('current_rates')