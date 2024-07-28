"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

# Aiogram
from aiogram.enums import ParseMode
from aiogram.types import Message

# Обработка команды
from process_command import process_command


# Событие /help
async def send_help(message: Message):
    HELP_TEXT = (
        'Доступные команды:\n'
        '1. /help - Список команд\n'
        '2. /info - Полезная информация\n'
        '3. /ms - Расчёт миллисекунд delay на основе BPM\nПример: /ms 120\n'
        '4. /ltsms - Delay база LTS\n'
    )
    await process_command(message, 'help', HELP_TEXT, ParseMode.HTML)


# Событие /info
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
    await process_command(message, 'info', INFO_TEXT, ParseMode.MARKDOWN)
