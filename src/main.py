"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

from datetime import datetime
import asyncio

# Aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Loguru
from logger import logger

# Конфигурация
from config import API_TOKEN, CHAT_ID, TOPIC_ID, RSS_TOPIC_ID, DOMAINS

# YouTube парсер
# from parsers.youtube import check_new_videos as yt_check_new_videos

# VK парсер
# from parsers.vk import check_new_posts as vk_check_new_posts


# Инициализация бота и диспетчера
bot = Bot(
    token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


# Функция проверки сообщений из правильного чата и темы
def is_valid_message(message: types.Message):
    return (
        message.chat.id == CHAT_ID
        and getattr(message, 'message_thread_id', None) == TOPIC_ID
    )


# Цикл приложения
async def main():
    try:
        now = datetime.now()
        formatted_date = now.strftime('%d/%m/%Y %H:%M:%S')
        logger.info(f'✔️ Запущен! {formatted_date}')

        await asyncio.gather(
            # Опрос бота
            dp.start_polling(bot),
            # Проверка видео на YouTube
            # yt_check_new_videos(bot, chat_id=CHAT_ID, rss_topic_id=RSS_TOPIC_ID),
            # Проверка постов в VK
            # vk_check_new_posts(
            #     bot,
            #     chat_id=CHAT_ID,
            #     rss_topic_id=RSS_TOPIC_ID,
            #     domains=DOMAINS,
            # ),
        )

    except (KeyboardInterrupt, SystemExit):
        logger.warning(f'⚠️ Отстановлен! {formatted_date}')


if __name__ == '__main__':
    asyncio.run(main())
