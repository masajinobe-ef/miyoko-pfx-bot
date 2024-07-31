"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

import asyncio
from datetime import datetime

# Aiogram
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Config
from config import API_TOKEN

# Loguru
from logger import logger

# Routers
from routers.cmds import info
from routers.parsers.livefans import livefans_affiche
from routers.tools import bpmtoms, calcs, ltsms

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
    try:
        logger.info(f'✅ Запущен! {now()}')

        # cmds
        (dp.include_router(info.router),)

        # tools
        (dp.include_router(calcs.router),)
        (dp.include_router(ltsms.router),)
        (dp.include_router(bpmtoms.router),)

        # parsers
        asyncio.create_task(livefans_affiche(bot))

        # Bot polling
        await dp.start_polling(bot)

    except (KeyboardInterrupt, SystemExit):
        logger.warning(f'❌ Отстановлен! {now()}')


if __name__ == '__main__':
    asyncio.run(main())
