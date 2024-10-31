from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
import math
from decimal import Decimal, getcontext
from handlers import process_group_commands


router = Router()
getcontext().prec = 10


def bpm_to_ms(bpm):
    if bpm <= 0:
        raise ValueError()

    one_beat_ms = Decimal(60000) / Decimal(bpm)
    note_durations = {
        '1/4': one_beat_ms,
        '1/8': one_beat_ms / Decimal(2),
        '1/16': one_beat_ms / Decimal(4),
        '1/32': one_beat_ms / Decimal(8),
        '1/64': one_beat_ms / Decimal(16),
        '1/128': one_beat_ms / Decimal(32),
    }
    return note_durations


def rc_low_pass_cutoff_frequency(R, C):
    if R <= 0 or C <= 0:
        raise ValueError()
    return Decimal(1) / (
        Decimal(2) * Decimal(math.pi) * Decimal(R) * Decimal(C)
    )


def db_to_voltage_ratio(dB):
    if dB <= 0:
        raise ValueError()
    return Decimal(10) ** (Decimal(dB) / Decimal(20))


def voltage_ratio_to_db(voltage_ratio):
    if voltage_ratio <= 0:
        raise ValueError()
    return Decimal(20) * Decimal(math.log10(voltage_ratio))


@router.message(Command(commands='cap'))
async def convert_capacitance(message: Message):
    try:
        input_values = message.text.split()[1:]
        if len(input_values) != 2:
            raise ValueError

        value_str, unit = input_values
        value = Decimal(value_str)

        if unit == 'u':
            nF = value * Decimal(1000)
            pF = value * Decimal(1000000)
            response_text = (
                f'✅Значения для {value} µF:\n{nF:.3f} nF\n{pF:.3f} pF'
            )
        elif unit == 'n':
            uF = value / Decimal(1000)
            pF = value * Decimal(1000)
            response_text = (
                f'✅Значения для {value} nF:\n{uF:.3f} µF\n{pF:.3f} pF'
            )
        elif unit == 'p':
            uF = value / Decimal(1000000)
            nF = value / Decimal(1000)
            response_text = (
                f'✅Значения для {value} pF:\n{uF:.3f} µF\n{nF:.3f} nF'
            )
        else:
            raise ValueError

    except (IndexError, ValueError):
        response_text = '⚠️Укажите корректные значения ёмкости и единицу измерения (u, n, p).\nПример: cap 10 u'

    await process_group_commands(message, 'cap', response_text, ParseMode.HTML)


@router.message(Command(commands='gain'))
async def calculate_expression(message: Message):
    try:
        input_values = message.text.split()[1:]
        if len(input_values) != 3:
            raise ValueError

        R1_str, R2_str, R3_str = input_values
        if (
            not R1_str.endswith('k')
            or not R2_str.endswith('k')
            or not R3_str.endswith('k')
        ):
            raise ValueError

        R1 = Decimal(R1_str[:-1]) * Decimal(1000)
        R2 = Decimal(R2_str[:-1]) * Decimal(1000)
        R3 = Decimal(R3_str[:-1]) * Decimal(1000)

        result = Decimal(1) + (R1 + R2) / R3

        voltage_ratio = (R1 + R2) / R3
        db_value = voltage_ratio_to_db(voltage_ratio)

        response_text = f'✅Результат: {result:.3f} (dB: {db_value:.3f})'

    except (IndexError, ValueError):
        response_text = '⚠️Укажите корректные значения R1, R2 и R3 (в kΩ).\nПример: gain 0k 500k 4.7k'

    await process_group_commands(
        message, 'gain', response_text, ParseMode.HTML
    )


@router.message(Command(commands='ms'))
async def send_ms(message: Message):
    try:
        bpm = int(message.text.split()[1])
        note_durations = bpm_to_ms(bpm)

    except IndexError:
        response_text = (
            '⚠️Укажите значение BPM после команды /ms.\nНапример: /ms 120'
        )
        await process_group_commands(
            message, 'ms', response_text, ParseMode.HTML
        )
        return

    except ValueError:
        response_text = '⚠️Значение BPM должно быть положительным числом.'
        await process_group_commands(
            message, 'ms', response_text, ParseMode.HTML
        )
        return

    response_text = f'✅Значения длительности нот для BPM = {bpm}:\n'
    for note, duration in note_durations.items():
        response_text += f'{note}: {duration:.3f} ms\n'

    await process_group_commands(message, 'ms', response_text, ParseMode.HTML)


@router.message(Command(commands='filter'))
async def send_filter(message: Message):
    try:
        input_values = message.text.split()[1:]
        if len(input_values) != 2:
            raise ValueError

        R_str, C_str = input_values
        if not R_str.endswith('k') or not C_str.endswith('n'):
            raise ValueError

        R = Decimal(R_str[:-1]) * Decimal(1000)  # Convert kΩ to Ω
        C = Decimal(C_str[:-1]) / Decimal(1000000000)  # Convert nF to F

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
        dB = Decimal(message.text.split()[1])
        voltage_gain = db_to_voltage_ratio(dB)
        response_text = f'✅Значение: {voltage_gain:.3f} V'

    except (IndexError, ValueError):
        response_text = '⚠️Укажите допустимое значение dB для преобразования.\nПример: dbV 10.0'

    await process_group_commands(message, 'dbV', response_text, ParseMode.HTML)


@router.message(Command(commands='Vdb'))
async def convert_voltage_to_db(message: Message):
    try:
        voltage_ratio = Decimal(message.text.split()[1])
        dB = voltage_ratio_to_db(voltage_ratio)
        response_text = f'✅Значение: {dB:.3f} dB'

    except (IndexError, ValueError):
        response_text = '⚠️Укажите допустимое напряжение для преобразования.\nПример: Vdb 10.0'

    await process_group_commands(message, 'Vdb', response_text, ParseMode.HTML)
