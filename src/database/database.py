"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

# SQLAlchemy
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

# Config
from config import ECHO_DB

# Loguru
from logger import logger

# Models
from database.models import Base


DATABASE_URL = 'sqlite+aiosqlite:///database.db'


async_engine = create_async_engine(DATABASE_URL, echo=ECHO_DB)
async_session = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


# Init database
async def init_db(db_name='database.db'):
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            # await conn.run_sync(Base.metadata.drop_all)
            logger.info('❕База данных и таблицы успешно инициализированы.')
    except ConnectionRefusedError as e:
        logger.error(f'❌ Ошибка подключения к базе данных: {e}')
