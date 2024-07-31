"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

# Aiogram
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

# Commands processing
from process_command import process_command

router = Router()


def bpm_to_ms(bpm):
    if bpm <= 0:
        raise ValueError()

    one_beat_ms = 60000 / bpm
    note_durations = {
        '1/4': one_beat_ms,
        '1/8': one_beat_ms / 2,
        '1/16': one_beat_ms / 4,
        '1/32': one_beat_ms / 8,
        '1/64': one_beat_ms / 16,
        '1/128': one_beat_ms / 32,
    }
    return note_durations


# Event /ms
@router.message(Command(commands='ms'))
async def send_ms(message: Message):
    try:
        bpm = int(message.text.split()[1])
        note_durations = bpm_to_ms(bpm)
    except IndexError:
        response_text = (
            '⚠️Укажите значение BPM после команды /ms.\nНапример: /ms 120'
        )
        await process_command(message, 'ms', response_text, ParseMode.HTML)
        return
    except ValueError:
        response_text = '⚠️Значение BPM должно быть положительным числом.'
        await process_command(message, 'ms', response_text, ParseMode.HTML)
        return

    response_text = f'✅Значения длительности нот для BPM = {bpm}:\n'
    for note, duration in note_durations.items():
        response_text += f'{note}: {duration:.3f} ms\n'
    await process_command(message, 'ms', response_text, ParseMode.HTML)
