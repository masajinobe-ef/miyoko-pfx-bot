"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

# SQLAlchemy
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Loguru
from logger import logger

# Models
Base = declarative_base()


class LiveFansAffiche(Base):
    __tablename__ = 'livefans_affiche'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    image = Column(String)
    description = Column(String)
    link = Column(String, unique=True)


class SigureInfo(Base):
    __tablename__ = 'sigure_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    image = Column(String)
    description = Column(String)
    link = Column(String, unique=True)


# Init
def init_db(db_name='database.db'):
    engine = create_engine(f'sqlite:///{db_name}')
    Base.metadata.create_all(engine)
    logger.info('База данных и таблицы успешно инициализированы.')


engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
