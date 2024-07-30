"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

import asyncio
import sqlite3
from datetime import datetime, timedelta

import pytz
import requests

# Web
from bs4 import BeautifulSoup

# Loguru
from loguru import logger

# Config
from config import CHAT_ID, RSS_TOPIC_ID

url = 'https://www.sigure.jp/info'


def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sigure_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            image TEXT,
            description TEXT,
            link TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()


def save_sigure_to_db(sigure):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO sigure_info (title, image, description, link)
            VALUES (?, ?, ?, ?)
            """,
            (
                sigure['title'],
                sigure['image'],
                sigure['description'],
                sigure['link'],
            ),
        )
        conn.commit()
    except Exception as e:
        logger.error(f'Ошибка при сохранении афиши в базу данных: {e}')
    finally:
        conn.close()


def fetch_sigure():
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим блок с информацией
        info_block = soup.find('div', id='info-block')
        if not info_block:
            logger.error('❌ Блок с информацией не найден.')
            return []

        # Находим все статьи в блоке
        articles = info_block.find_all('article')
        posts = []

        for article in articles:
            # Получаем время и заголовок
            time_tag = article.find('time')
            h1_tag = article.find('h1')
            time_text = time_tag['datetime'] if time_tag else None
            title_text = h1_tag.text if h1_tag else None

            # Получаем текст и ссылки из блока с классом "block-body mincho"
            block_body = article.find('div', class_='block-body mincho')
            body_text = block_body.text.strip() if block_body else None
            links = (
                [a['href'] for a in block_body.find_all('a', href=True)]
                if block_body
                else []
            )
            img_tag = block_body.find('img')
            img_src = img_tag['src'] if img_tag else None

            # Формируем полный пост
            posts.append(
                {
                    'title': title_text,
                    'time': time_text,
                    'image': img_src,
                    'description': body_text,
                    'links': links,
                }
            )
        return posts
    except Exception as e:
        logger.error(f'❌ Ошибка при получении: {e}')
        return []


async def sigure_info(bot):
    init_db()
    while True:
        tokyo_tz = pytz.timezone('Asia/Tokyo')
        now = datetime.now(tokyo_tz)
        next_midnight = now.replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + timedelta(days=1)
        wait_time = (next_midnight - now).total_seconds()

        logger.info(
            'Ожидание до следующей проверки sigure.jp в полночь по японскому времени.'
        )
        await asyncio.sleep(wait_time)  # Ждем до следующей полуночи

        new_sigure = fetch_sigure()
        logger.info('ⓘ Начинаем отправку постов с sigure.jp')
        for sigure in new_sigure:
            save_sigure_to_db(sigure)

            try:
                await bot.send_message(
                    chat_id=CHAT_ID,
                    message_thread_id=RSS_TOPIC_ID,
                    text=f'Новая информация с sigure.jp опубликована!\n\n**{sigure["title"]}**\n{sigure["description"]}\n[Ссылка на пост]({sigure["link"]})',
                    parse_mode='MARKDOWN',
                )
            except Exception as e:
                logger.error(f'❌ Ошибка при отправке сообщения: {e}')

        logger.info('ⓘ Завершена отправка новых постов с sigure.jp.')
