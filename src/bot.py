# import os
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import API_TOKEN
from logger import logger

# from database import init_db
from routers.tools import calc
from routers.cmds import info
from routers.events import events
# from routers.cmds import direct
# from routers.parsers.livefans import livefans_affiche


bot = Bot(
    token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


def now():
    now = datetime.now()
    formatted_date = now.strftime('%d/%m/%Y %H:%M:%S')
    return formatted_date


async def main():
    # if not os.path.exists('database.db'):
    #     await init_db()
    #     logger.info('ℹ️ База данных инициализирована впервые.')

    logger.info(f'✅ Запущен! {now()}')

    # Cmds
    (dp.include_router(info.router),)
    # (dp.include_router(direct.router),)

    # Tools
    (dp.include_router(calc.router),)

    # Events
    (dp.include_router(events.router),)

    # Parsers
    # asyncio.create_task(livefans_affiche(bot))

    # Bot polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning(f'⚠️ Отстановлен! {now()}')
