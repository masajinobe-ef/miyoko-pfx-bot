"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Models
from models import Base

# Loguru
from logger import logger


engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()


# Init Database
def init_db(db_name='database.db'):
    engine = create_engine(f'sqlite:///{db_name}')
    Base.metadata.create_all(engine)
    logger.info('❕База данных и таблицы успешно инициализированы.')


# Functions
def is_database_empty(model):
    count = session.query(model).count()
    session.close()
    return count == 0


def row_exists(model, **kwargs):
    exists = session.query(model).filter_by(**kwargs).first() is not None
    session.close()
    return exists
