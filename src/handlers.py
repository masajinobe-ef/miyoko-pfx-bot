"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

# Aiogram
from aiogram.filters import Command

# Функции
from func.basic.info import send_help, send_info
from func.tools.bpmtoms import send_ms
from func.tools.ltsms import send_ltsms
# Loguru
from logger import logger


def register_handlers(dp):
    dp.include_router(send_info, Command(commands=['info']))
    dp.include_router(send_help, Command(commands=['help']))
    dp.include_router(send_ms, Command(commands=['ms']))
    dp.include_router(send_ltsms, Command(commands=['ltsms']))
    logger.info('✔️ Обработчики определены')
