"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

from datetime import datetime

# Loguru
from loguru import logger


def now():
    return datetime.now().strftime('%d-%m-%Y')


# Info
logger.add(
    f'logs/{now()}_miyoko.log',
    rotation='00:00',
    retention='1 day',
    level='INFO',
    format='{time:DD/MM/YYYY HH:mm:ss} | {level} | {message}',
)


# Warning
logger.add(
    f'logs/{now()}_miyoko.log',
    rotation='00:00',
    retention='1 day',
    level='WARNING',
    format='{time:DD/MM/YYYY HH:mm:ss} | {level} | {message}',
)

# Error
logger.add(
    f'logs/{now()}_miyoko.log',
    rotation='00:00',
    retention='1 day',
    level='ERROR',
    format='{time:DD/MM/YYYY HH:mm:ss} | {level} | {message}',
)
