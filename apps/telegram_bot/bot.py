import os
import logging
from telegram import Bot
from telegram.error import TelegramError

logger = logging.getLogger(__name__)

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
if not bot_token:
    logger.error('TELEGRAM_BOT_TOKEN не установлен!')
    bot = None
else:
    bot = Bot(token=bot_token)

async def send_message(chat_id:int, text:str):
    if bot is None:
        logger.error('Бот не инициализирован')
        return
    try:
        await bot.send_message(chat_id=chat_id, text=text)
        logger.info(f'Сообщение отправлено пользователю {chat_id}')
    except TelegramError as e:
        logger.error(f'Ошибка отправки в Telegram: {e}')
        raise