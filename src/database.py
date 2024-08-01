"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

# SQLAlchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Config
from config import ECHO_DB

# Loguru
from logger import logger

# Models
from models import Base


DATABASE_URL = 'sqlite+aiosqlite:///database.db'


# Init database
async def init_db(db_name='database.db'):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info('❕База данных и таблицы успешно инициализированы.')


engine = create_async_engine(DATABASE_URL, echo=ECHO_DB)
SessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Functions
# async def is_database_empty(model):
#     count = session.query(model).count()
#     session.close()
#     return count == 0

# async def row_exists(model, **kwargs):
#     exists = session.query(model).filter_by(**kwargs).first() is not None
#     session.close()
#     return exists
