from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


def now():
    return datetime.now(timezone.utc)


class LiveFansAffiche(Base):
    __tablename__ = 'livefans_affiche'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    image = Column(String)
    description = Column(String)
    link = Column(String, unique=True)


class LiveFansURL(Base):
    __tablename__ = 'livefans_urls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    url = Column(String, unique=True)


class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)
    invoice_payload = Column(String, nullable=False)
    telegram_payment_charge_id = Column(String, nullable=False)
    provider_payment_charge_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=now)
