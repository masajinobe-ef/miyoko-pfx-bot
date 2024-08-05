"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

import os
import asyncio
from datetime import datetime

# Aiogram
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Config
from config import API_TOKEN

# Database
# from database import init_db

# Loguru
from logger import logger

# Routers
from routers.tools import calc
from routers.cmds import info
# from routers.cmds import direct
# from routers.parsers.livefans import livefans_affiche


# Bot and Dispatcher
bot = Bot(
    token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


def now():
    now = datetime.now()
    formatted_date = now.strftime('%d/%m/%Y %H:%M:%S')
    return formatted_date


# Lifespan
async def main():
    # Database
    # if not os.path.exists('database.db'):
    #     await init_db()
    #     logger.info('ℹ️ База данных инициализирована впервые.')

    logger.info(f'✅ Запущен! {now()}')

    # Cmds
    (dp.include_router(info.router),)
    # (dp.include_router(direct.router),)

    # Tools
    (dp.include_router(calc.router),)

    # Parsers
    # asyncio.create_task(livefans_affiche(bot))

    # Bot polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning(f'⚠️ Отстановлен! {now()}')
