from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_2fa_code(user_id, telegram_id, code):
    logger.info(f"[2FA] Отправка 2FA кода {code} пользователю {user_id} (Telegram ID: {telegram_id})")