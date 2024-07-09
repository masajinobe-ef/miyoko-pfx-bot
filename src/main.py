"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

import asyncio
import yaml

# Aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command

# Loguru
from logger import logger

# Parser
# from parser import check_new_videos


# Config file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

API_TOKEN = config['bot']['token']
CHAT_ID = config['bot']['chat_id']
TOPIC_ID = int(config['bot']['topic_id'])


# Init Bot
bot = Bot(
    token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


# Function to check if the message is from the correct chat and topic
def is_valid_message(message: types.Message):
    return (
        message.chat.id == CHAT_ID
        and getattr(message, 'message_thread_id', None) == TOPIC_ID
    )


# Helper function to process commands
async def process_command(message: types.Message, command: str, response: str):
    if not is_valid_message(message) or not message.text.startswith('/'):
        return
    logger.info(
        f'✉️ Получена команда: /{command} от {message.from_user.username} ({message.from_user.id})'
    )
    await message.reply(response, parse_mode=ParseMode.HTML)


# Command responses
help_text = (
    'Доступные команды:\n\n'
    '/help - Список команд\n'
    '/info - Полезная информация'
)

info_text = (
    '✉️ Связаться с нами: https://t.me/masaji_ef\n\n'
    '❔ Часто задаваемые вопросы: https://priscillafx.ru/faq\n\n'
    '▇ Официальный сайт: https://priscilla-custom-effects.github.io/\n\n'
    '▇ Социальные сети:\n'
    '- VK: https://vk.com/priscilla_ef\n'
    '- Instagram: https://www.instagram.com/masajinobe\n'
    '- Twitter: https://twitter.com/priscilla_eF\n'
    '- GitHub: https://github.com/Priscilla-Custom-Effects\n'
    '- YouTube: https://www.youtube.com/@priscilla_eF'
)


# Event /help
@dp.message(Command(commands=['help']))
async def send_help(message: types.Message):
    await process_command(message, 'help', help_text)


# Event /info
@dp.message(Command(commands=['info']))
async def send_info(message: types.Message):
    await process_command(message, 'info', info_text)


# Unknown commands
@dp.message()
async def echo(message: types.Message):
    if not is_valid_message(message) or not message.text.startswith('/'):
        return
    logger.info(
        f'⚠️ Нераспознанная команда: {message.text} от {message.from_user.username}'
    )
    await message.reply(
        '⚠️ Неизвестная команда. Напишите /help для получения списка команд.',
        parse_mode=ParseMode.HTML,
    )


async def main():
    try:
        logger.info('Запущен!')

        # Start polling and YouTube video checking concurrently
        await asyncio.gather(
            dp.start_polling(bot),
            # check_new_videos(bot, chat_id=CHAT_ID)
        )

    except (KeyboardInterrupt, SystemExit):
        logger.warning('Отстановлен!')


if __name__ == '__main__':
    asyncio.run(main())
