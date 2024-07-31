"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

# Aiogram
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

# Commands processing
from process_command import process_command

router = Router()


# Event /help
@router.message(Command(commands='help'))
async def send_help(message: Message):
    HELP_TEXT = (
        'Информация:\n'
        '⚪ /help - Список команд\n'
        '⚪ /info - Полезная информация\n'
        '⚪ /ltsms - Дилей база LTS\n'
        '\n'
        'Инструменты:\n'
        '⚪ /ms - Расчёт миллисекунд задержки на основе BPM\nПример: ms 120\n'
        '⚪ /filter - Расчёт RC-фильтра. Пример: filter 1.0k 1.0n\n'
        '⚪ /dbV - Конвертер db в V. Пример: dbV 10.0\n'
        '⚪ /Vdb - Конвертер V в db. Пример: Vdb 10.0\n'
    )
    await process_command(message, 'help', HELP_TEXT, ParseMode.MARKDOWN)


# Event /info
@router.message(Command(commands='info'))
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
        '⚪ [YouTube](https://www.youtube.com/@priscilla_eF)\n'
    )
    await process_command(message, 'info', INFO_TEXT, ParseMode.MARKDOWN)
