"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

# Aiogram
from aiogram.filters import Command
from aiogram.exceptions import TelegramNotFound
from aiogram.enums import ParseMode
from aiogram.types import Message

# Loguru
from logger import logger

# Зависимость от main.py
from main import dp, is_valid_message

# BPM to ms
# from func.bpmtoms import bpm_to_ms


# Вспомогательная функция для обработки команд
async def process_command(message: Message, command: str, response: str):
    if not is_valid_message(message) or not message.text.startswith('/'):
        return

    logger.info(
        f'✉️ Получена команда: /{command} от {message.from_user.username} ({message.from_user.id})'
    )

    try:
        await message.reply(response, parse_mode=ParseMode.MARKDOWN)
    except TelegramNotFound:
        logger.warning(
            f'⚠️ Сообщение удалено: не удалось ответить на команду /{command}'
        )


# Событие /help
@dp.message(Command(commands=['help']))
async def send_help(message: Message):
    HELP_TEXT = (
        'Доступные команды:\n'
        '1. /help - Список команд\n'
        '2. /info - Полезная информация'
    )
    await process_command(message, 'help', HELP_TEXT)


# Событие /info
@dp.message(Command(commands=['info']))
async def send_info(message: Message):
    INFO_TEXT = (
        '✉️ [Связаться с нами](https://t.me/masaji_ef)\n'
        '❔ [Часто задаваемые вопросы](https://priscillafx.ru/faq)\n'
        '🌐 [Официальный сайт](https://priscilla-custom-effects.github.io/)\n'
        'Социальные сети:\n'
        '⚪ [VK](https://vk.com/priscilla_ef)\n'
        '⚪ [Instagram](https://www.instagram.com/masajinobe)\n'
        '⚪ [Twitter](https://twitter.com/priscilla_eF)\n'
        '⚪ [GitHub](https://github.com/Priscilla-Custom-Effects)\n'
        '⚪ [YouTube](https://www.youtube.com/@priscilla_eF)'
    )
    await process_command(message, 'info', INFO_TEXT)


# Событие /ms
# @dp.message(Command(commands=['ms']))
# async def send_ms(message: types.Message):
#     match = re.search(r'/ms\s+(\d+)', message.text)
#     if not match:
#         await message.reply(
#             'Пожалуйста, предоставьте BPM значение после команды /ms, например: /ms 120'
#         )
#         return

#     bpm = int(match.group(1))
#     note_durations = bpm_to_ms(bpm)

#     response_text = 'Значения длительности нот для BPM = {}:\n'.format(bpm)
#     for note, duration in note_durations.items():
#         response_text += f'{note}: {duration:.2f} ms\n'

#     await process_command(message, 'ms', response_text)


# Неизвестная команда
@dp.message()
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
