"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

# SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Models
Base = declarative_base()


class LiveFansAffiche(Base):
    __tablename__ = 'livefans_affiche'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    image = Column(String)
    description = Column(String)
    link = Column(String, unique=True)


class LiveFansURLs(Base):
    __tablename__ = 'livefans_urls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    url = Column(String, unique=True)
