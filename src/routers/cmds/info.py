"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

# Aiogram
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

# Command handler
from command_handler import process_group_commands

router = Router()


# Event /help
@router.message(Command(commands='help'))
async def send_help(message: Message):
    HELP_TEXT = (
        '<b>Информация:</b>\n'
        '● /help – Список команд.\n'
        '● /info – Полезная информация.\n'
        '\n'
        '<b>Расчёты:</b>\n'
        '● /ms – Миллисекунды задержки на основе BPM <i>(ms 120)</i>.\n'
        '● /filter – RC-фильтр <i>(filter 1.0k 1.0n)</i>.\n'
        '● /gain – Voltage Gain по формуле 1 + (R1 + R2) / R3\n<i>(gain 0k 500k 4.7k)</i>.\n'
        '\n'
        '<b>Конвертеры:</b>\n'
        '● /cap – Ёмкости конденсатора <i>(cap 10 u)</i>.\n'
        '● /dbV – db в V <i>(dbV 10.0)</i>.\n'
        '● /Vdb – V в db <i>(Vdb 10.0)</i>.\n'
    )
    await process_group_commands(message, 'help', HELP_TEXT, ParseMode.HTML)


# Event /info
@router.message(Command(commands='info'))
async def send_info(message: Message):
    INFO_TEXT = (
        '<b>Основное:</b>\n'
        '✉️ <a href="https://t.me/masaji_ef">Связаться с нами</a>\n'
        '❔ <a href="https://priscillafx.ru/faq">Часто задаваемые вопросы</a>\n'
        '🌐 <a href="https://priscilla-custom-effects.github.io/">Официальный сайт</a>\n'
        '\n'
        '<b>Социальные сети:</b>\n'
        '● <a href="https://vk.com/priscilla_ef">VK</a>\n'
        '● <a href="https://www.instagram.com/masajinobe">Instagram</a>\n'
        '● <a href="https://twitter.com/priscilla_eF">Twitter</a>\n'
        '● <a href="https://github.com/Priscilla-Custom-Effects">GitHub</a>\n'
        '● <a href="https://www.youtube.com/@priscilla_eF">YouTube</a>\n'
    )
    await process_group_commands(message, 'info', INFO_TEXT, ParseMode.HTML)
