"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

# Aiogram
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramNotFound
from aiogram.types import Message

# Config
from config import CHAT_ID, DOMAINS, RSS_TOPIC_ID, TOPIC_ID
# Loguru
from logger import logger


# Valid messages
def is_valid_message(message: Message):
    return (
        message.chat.id == CHAT_ID
        and getattr(message, 'message_thread_id', None) == TOPIC_ID
    )


# Commands processing
async def process_command(
    message: Message, command: str, response: str, parse_mode: ParseMode
):
    if not is_valid_message(message) or not message.text.startswith('/'):
        return
    logger.info(
        f'✉️ Получена команда: /{command} от {message.from_user.username} ({message.from_user.id})'
    )
    try:
        await message.reply(response, parse_mode=parse_mode)
    except TelegramNotFound:
        logger.warning(
            f'⚠️ Сообщение удалено: не удалось ответить на команду /{command}'
        )


# Unknown command
async def echo(message: Message):
    if not is_valid_message(message) or not message.text.startswith('/'):
        return
    try:
        await message.reply(
            '⚠️ Неизвестная команда. Напишите /help для получения списка команд.',
            parse_mode=ParseMode.HTML,
        )
        logger.info(
            f'⚠️ Нераспознанная команда: {message.text} от {message.from_user.username}'
        )
    except TelegramNotFound:
        logger.warning(
            f'⚠️ Сообщение удалено: не удалось ответить на неизвестную команду {message.text}'
        )
