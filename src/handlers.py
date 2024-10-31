from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramNotFound
from aiogram.types import Message
from config import CHAT_ID, TOPIC_ID
from logger import logger


def is_group_message(message: Message):
    return (
        message.chat.id == CHAT_ID
        and getattr(message, 'message_thread_id', None) == TOPIC_ID
    )


async def process_group_commands(
    message: Message, command: str, response: str, parse_mode: ParseMode
):
    if not is_group_message(message) or not message.text.startswith('/'):
        return
    logger.info(
        f'✉️  Group: /{command} от {message.from_user.username} ({message.from_user.id})'
    )

    try:
        await message.reply(response, parse_mode=parse_mode)

    except TelegramNotFound:
        logger.warning(
            f'ℹ️ Сообщение в группе удалено: не удалось ответить на команду /{command} от {message.from_user.username} ({message.from_user.id})'
        )


async def process_direct_commands(
    message: Message, command: str, response: str, parse_mode: ParseMode
):
    if is_group_message(message) or not message.text.startswith('/'):
        return
    logger.info(
        f'✉️  DM: /{command} от {message.from_user.username} ({message.from_user.id})'
    )

    try:
        await message.reply(response, parse_mode=parse_mode)

    except TelegramNotFound:
        logger.warning(
            f'ℹ️ Сообщение в DM удалено: не удалось ответить на команду /{command} от {message.from_user.username} ({message.from_user.id})'
        )


async def echo(message: Message):
    if not is_group_message(message) or not message.text.startswith('/'):
        return
    try:
        await message.reply(
            '⚠️Неизвестная команда. Напишите /help для получения списка команд.',
            parse_mode=ParseMode.HTML,
        )
        logger.info(
            f'⚠️ Нераспознанная команда: {message.text} от {message.from_user.username}'
        )

    except TelegramNotFound:
        logger.warning(
            f'⚠️ Сообщение удалено: не удалось ответить на неизвестную команду {message.text}'
        )
