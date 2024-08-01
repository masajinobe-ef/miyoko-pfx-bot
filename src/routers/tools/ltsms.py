"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

# Aiogram
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

# Command handler
from command_handler import process_group_commands

router = Router()


# Event /ltsms
@router.message(Command(commands='ltsms'))
async def send_ltsms(message: Message):
    LTSMS_TEXT = (
        '*#4:*\n'
        '_-_-_-_-_-_-_-_-_-_\n'
        '鮮やかな殺人\n'
        'テレキャスターの真実\n'
        'Sadistic Summer\n'
        'ターボチャージャーON | BPM132 / 340ms\n'
        'Acoustic\n'
        'O.F.T | BPM131 / 343ms\n'
        'CRAZY感情STYLE | BPM124 / 362ms\n'
        'トルネードG\n'
        '傍観\n'
        'TK in the 夕景\n'
        '\n'
        '*Feeling your UFO:*\n'
        '_-_-_-_-_-_-_-_-_-_\n'
        '想像のSecurity\n'
        '感覚UFO\n'
        '秋の気配のアルペジオ\n'
        'ラストダンスレボリューション\n'
        'Sergio Echigo\n'
        '\n'
        '*Inspiration is DEAD:*\n'
        '_-_-_-_-_-_-_-_-_-_\n'
        'nakano kill you\n'
        'COOL J\n'
        'DISCO FLIGHT | BPM135 / 333ms\n'
        'knife vacation\n'
        'am3:45\n'
        '赤い誘惑\n'
        '1/fの感触\n'
        'i not crazy am you are\n'
        '夕景の記憶 | BPM83 / 361ms\n'
        '\n'
        '*Inspiration is DEAD:*\n'
        '_-_-_-_-_-_-_-_-_-_\n'
        'nakano kill you\n'
        'COOL J\n'
        'DISCO FLIGHT | BPM135 / 333ms\n'
        'knife vacation\n'
        'am3:45\n'
        '赤い誘惑\n'
        '1/fの感触\n'
        'i not crazy am you are\n'
        '夕景の記憶 | BPM83 / 361ms\n'
    )
    PLACEHOLDER = 'placeholder'
    await process_group_commands(message, 'ltsms', PLACEHOLDER, ParseMode.HTML)
