import asyncio
import logging
from celery import shared_task
from .bot import send_message

logger = logging.getLogger(__name__)

@shared_task
def send_2fa_code(user_id: int, telegram_id: int, code: str):
    """Отправляет пользователю 2FA код через Telegram"""

    logger.info(f'Задача send_2fa_code: user_id={user_id}, telegram_id={telegram_id}, code={code}')
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(send_message(telegram_id, f'Ваш код для входа: {code}'))
