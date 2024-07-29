"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

import math

# Aiogram
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

# Commands processing
from process_command import process_command

router = Router()


def rc_low_pass_cutoff_frequency(R, C):
    return 1 / (2 * math.pi * R * C)


def db_to_voltage_ratio(dB):
    return 10 ** (dB / 20)


def voltage_ratio_to_db(voltage_ratio):
    return 20 * math.log10(voltage_ratio)


# Event /filter
@router.message(Command(commands='filter'))
async def send_filter(message: Message):
    try:
        input_values = message.text.split()[1:]
        if len(input_values) != 2:
            raise ValueError

        R_str, C_str = input_values
        if not R_str.endswith('k') or not C_str.endswith('n'):
            raise ValueError

        R = float(R_str[:-1]) * 1000  # Convert kΩ to Ω
        C = float(C_str[:-1]) / 1000000000  # Convert nF to F
    except (IndexError, ValueError):
        response_text = '⚠️ Пожалуйста, укажите значения R (в kΩ) и C (в nF).\nПример: /filter 1k 1n'
        await process_command(message, 'filter', response_text, ParseMode.HTML)
        return

    cut_off_frequency = rc_low_pass_cutoff_frequency(R, C)
    response_text = 'Частоты среза RC-фильтра: {:.3f} Hz'.format(
        cut_off_frequency
    )
    await process_command(message, 'filter', response_text, ParseMode.HTML)


@router.message(Command(commands='dbV'))
async def convert_db_to_voltage(message: Message):
    try:
        dB = float(message.text.split()[1])
        voltage_gain = db_to_voltage_ratio(dB)
        response_text = f'{dB:.3f} dB: {voltage_gain:.3f}'
    except (IndexError, ValueError):
        response_text = (
            '⚠️ Пожалуйста, укажите допустимое значение dB для преобразования.'
        )

    await process_command(message, 'dbV', response_text, ParseMode.HTML)


@router.message(Command(commands='Vdb'))
async def convert_voltage_to_db(message: Message):
    try:
        voltage_ratio = float(message.text.split()[1])
        dB = voltage_ratio_to_db(voltage_ratio)
        response_text = f'{voltage_ratio:.3f} V: {dB:.3f}'
    except (IndexError, ValueError):
        response_text = (
            '⚠️ Пожалуйста, укажите допустимое напряжение для преобразования.'
        )

    await process_command(message, 'Vdb', response_text, ParseMode.HTML)
