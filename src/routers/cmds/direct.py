"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

import os

# Aiogram
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    LabeledPrice,
    PreCheckoutQuery,
)
from aiogram.enums import ParseMode

# Database
from database import init_db, SessionLocal

# Loguru
from logger import logger

# Config
from config import PAYMENTS_TOKEN

# Models
from database.models import Payment

# Command handler
from command_handler import process_direct_commands, is_group_message

router = Router()


# Event /start
@router.message(Command(commands='start'))
async def start_command(message: Message):
    if is_group_message(message) or not message.text.startswith('/'):
        return

    INFO_TEXT = (
        '✉️ [Связаться с нами](https://t.me/masaji_ef)\n'
        '❔ [Часто задаваемые вопросы](https://priscillafx.ru/faq)\n'
        '🌐 [Официальный сайт](https://priscillafx.ru)\n'
        'Социальные сети:\n'
        '⚪ [VK](https://vk.com/priscilla_ef)\n'
        '⚪ [Instagram](https://www.instagram.com/masajinobe)\n'
        '⚪ [Twitter](https://twitter.com/priscilla_eF)\n'
        '⚪ [GitHub](https://github.com/Priscilla-Custom-Effects)\n'
        '⚪ [YouTube](https://www.youtube.com/@priscilla_eF)\n'
    )
    await process_direct_commands(
        message, 'start', INFO_TEXT, ParseMode.MARKDOWN
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🛒 Купить софт', callback_data='buy_soft'
                ),
                InlineKeyboardButton(
                    text='💼 Услуга', callback_data='buy_service'
                ),
                InlineKeyboardButton(
                    text='💴 Меценат',
                    callback_data='pay_donate',
                ),
            ]
        ]
    )
    await message.answer('Выберите опцию:', reply_markup=keyboard)


# Callbacks
@router.callback_query(lambda c: c.data == 'buy_soft')
async def process_buy_soft(callback_query):
    if is_group_message(callback_query.message):
        return

    await process_direct_commands(
        callback_query.message,
        'buy_soft',
        '🛒 Купить софт',
        ParseMode.MARKDOWN,
    )


@router.callback_query(lambda c: c.data == 'buy_service')
async def process_buy_service(callback_query):
    if is_group_message(callback_query.message):
        return

    await process_direct_commands(
        callback_query.message, 'buy_service', '💼 Услуга', ParseMode.MARKDOWN
    )


@router.callback_query(lambda c: c.data == 'pay_donate')
async def process_pay_donate(callback_query):
    if is_group_message(callback_query.message):
        return

    await callback_query.answer('💴 Меценат')

    # Price
    RUB = 60
    DONATION_PRICE = LabeledPrice(
        label='Поддержка 「 Priscilla FX 」', amount=RUB * 100
    )

    try:
        await callback_query.message.answer_invoice(
            title='💴 Меценат',
            description='Поддержите проект 「 Priscilla FX 」',
            payload='donation_payload',
            provider_token=PAYMENTS_TOKEN,
            currency='rub',
            prices=[DONATION_PRICE],
            start_parameter='donate',
            photo_url='https://i.imgur.com/shFt6Iq.jpeg',
            photo_size=512,
            photo_width=512,
            photo_height=512,
            is_flexible=False,
        )

    except Exception as e:
        await callback_query.answer(f'Ошибка при отправке счета: {str(e)}')


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query_handler(pre_checkout_q: PreCheckoutQuery):
    await pre_checkout_q.answer(ok=True)


async def save_payment_to_db(payment_info, user):
    if not os.path.exists('database.db'):
        await init_db()
        logger.info('ℹ️ База данных инициализирована впервые. Запись платежа.')

    async with SessionLocal() as session:
        try:
            new_payment = Payment(
                username=user.username,
                user_id=user.id,
                currency=payment_info.currency,
                total_amount=payment_info.total_amount // 100,
                invoice_payload=payment_info.invoice_payload,
                telegram_payment_charge_id=payment_info.telegram_payment_charge_id,
                provider_payment_charge_id=payment_info.provider_payment_charge_id,
            )
            session.add(new_payment)
            await session.commit()

        except Exception as e:
            logger.error(
                f'❌ Ошибка при сохранении платежа в базу данных: {e}'
            )
            await session.rollback()
        finally:
            await session.close()


# successful payment
@router.message(F.successful_payment)
async def successful_payment(message: Message):
    if is_group_message(message):
        return

    logger.info(
        f'💴  Донат от пользователя {message.from_user.username} ({message.from_user.id})'
    )
    username = message.from_user.username
    user_id = message.from_user.id
    payment_info = message.successful_payment
    currency = payment_info.currency
    total_amount = payment_info.total_amount // 100
    invoice_payload = payment_info.invoice_payload
    telegram_payment_charge_id = payment_info.telegram_payment_charge_id
    provider_payment_charge_id = payment_info.provider_payment_charge_id
    shipping_option_id = payment_info.shipping_option_id
    order_info = payment_info.order_info
    formatted_payment_info = (
        f'Детали платежа:\n'
        f'👤 Пользователь: @{username} (ID: {user_id})\n'
        f'💰 Валюта: {currency}\n'
        f'💵 Сумма: {total_amount} {currency}\n'
        f'📄 Платежный инвойс: {invoice_payload}\n'
        f'🔒 Telegram ID платежа: {telegram_payment_charge_id}\n'
        f'🔑 ID провайдера платежа: {provider_payment_charge_id}\n'
    )
    if shipping_option_id:
        formatted_payment_info += (
            f'📦 ID опции доставки: {shipping_option_id}\n'
        )
    if order_info:
        formatted_payment_info += f'📝 Информация о заказе: {order_info}\n'
    logger.info(formatted_payment_info)

    await save_payment_to_db(payment_info, message.from_user)

    total_amount = payment_info.total_amount // 100
    currency = payment_info.currency

    await message.answer(
        f'Платеж на сумму {total_amount} {currency} прошел успешно!\nСпасибо за поддержку проекта 「 Priscilla FX 」 !',
        parse_mode=ParseMode.MARKDOWN,
    )
