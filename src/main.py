"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

import asyncio
from datetime import datetime

# Aiogram
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Обработчик
import handlers

# Конфигурация
from config import API_TOKEN

# Loguru
from logger import logger

# Инициализация бота и диспетчера
bot = Bot(
    token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


# Цикл приложения
async def main():
    try:
        now = datetime.now()
        formatted_date = now.strftime('%d/%m/%Y %H:%M:%S')
        logger.info(f'✔️ Запущен! {formatted_date}')

        # Регистрация обработчика команд
        handlers.register_handlers(dp)

        await asyncio.gather(
            # Опрос бота
            dp.start_polling(bot),
            # Проверка видео на YouTube
            # yt_check_new_videos(
            #     bot, chat_id=CHAT_ID, rss_topic_id=RSS_TOPIC_ID
            # ),
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
