"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

import math

# Aiogram
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

# Command handler
from command_handler import process_group_commands

router = Router()


# Calculation
def rc_low_pass_cutoff_frequency(R, C):
    if R <= 0 or C <= 0:
        raise ValueError()
    return 1 / (2 * math.pi * R * C)


def db_to_voltage_ratio(dB):
    if dB <= 0:
        raise ValueError()
    return 10 ** (dB / 20)


def voltage_ratio_to_db(voltage_ratio):
    if voltage_ratio <= 0:
        raise ValueError()
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

        cut_off_frequency = rc_low_pass_cutoff_frequency(R, C)
        response_text = '✅Частоты среза RC-фильтра: {:.3f} Hz'.format(
            cut_off_frequency
        )

    except (IndexError, ValueError):
        response_text = '⚠️Укажите корректные значения R (в kΩ) и C (в nF).\nПример: filter 1k 1n'

    await process_group_commands(
        message, 'filter', response_text, ParseMode.HTML
    )


@router.message(Command(commands='dbV'))
async def convert_db_to_voltage(message: Message):
    try:
        dB = float(message.text.split()[1])
        voltage_gain = db_to_voltage_ratio(dB)
        response_text = f'✅Значение: {voltage_gain:.3f} V'

    except (IndexError, ValueError):
        response_text = '⚠️Укажите допустимое значение dB для преобразования.\nПример: dbV 10.0'

    await process_group_commands(message, 'dbV', response_text, ParseMode.HTML)


@router.message(Command(commands='Vdb'))
async def convert_voltage_to_db(message: Message):
    try:
        voltage_ratio = float(message.text.split()[1])
        dB = voltage_ratio_to_db(voltage_ratio)
        response_text = f'✅Значение: {dB:.3f} db'

    except (IndexError, ValueError):
        response_text = '⚠️Укажите допустимое напряжение для преобразования.\nПример: Vdb 10.0'

    await process_group_commands(message, 'Vdb', response_text, ParseMode.HTML)
