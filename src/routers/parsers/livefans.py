"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

import asyncio
from datetime import datetime, timedelta

import pytz
import requests
# Web
from bs4 import BeautifulSoup
# Loguru
from loguru import logger

# Config
from config import CHAT_ID, RSS_TOPIC_ID
# Database
from database import LiveFansAffiche, Session, init_db

url = 'https://www.livefans.jp/search?option=1&keyword=%E5%87%9B%E3%81%A8%E3%81%97%E3%81%A6%E6%99%82%E9%9B%A8&genre=all&sort=e1'


def save_affiche_to_db(affiche):
    session = Session()
    try:
        new_affiche = LiveFansAffiche(
            title=affiche['title'],
            image=affiche['image'],
            description=affiche['description'],
            link=affiche['link'],
        )
        session.add(new_affiche)
        session.commit()
    except Exception as e:
        logger.error(
            f'❌ Ошибка при сохранении афиши c livefans.jp в базу данных: {e}'
        )
        session.rollback()
    finally:
        session.close()


def fetch_affiche():
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all(
            'div', class_=['whiteBack midBox fes', 'whiteBack midBox']
        )
        posts = []
        for element in elements:
            h3_tag = element.find('h3').text if element.find('h3') else None
            img_tag = (
                element.find('img')['src'] if element.find('img') else None
            )
            p_tag = element.find('p').text if element.find('p') else None
            a_tag = element.find('a')['href'] if element.find('a') else None
            full_link = f'https://www.livefans.jp{a_tag}' if a_tag else None
            posts.append(
                {
                    'title': h3_tag,
                    'image': img_tag,
                    'description': p_tag,
                    'link': full_link,
                }
            )
        return posts
    except Exception as e:
        logger.error(f'❌ Ошибка при получении афиш с livefans.jp: {e}')
        return []


async def livefans_affiche(bot):
    init_db()
    logger.info('ⓘ Начинаем проверку новых афиш с livefans.jp.')
    await check_and_send_affiches(bot)

    while True:
        tokyo_tz = pytz.timezone('Asia/Tokyo')
        now = datetime.now(tokyo_tz)
        next_midnight = now.replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + timedelta(days=1)
        wait_time = (next_midnight - now).total_seconds()

        logger.info(
            'ⓘ Ожидание до следующей проверки афиш с livefans.jp в полночь по японскому времени.'
        )
        await asyncio.sleep(wait_time)

        await check_and_send_affiches(bot)


def affiche_exists(link):
    session = Session()
    exists = (
        session.query(LiveFansAffiche).filter_by(link=link).first() is not None
    )
    session.close()
    return exists


async def check_and_send_affiches(bot):
    new_affiche = fetch_affiche()
    for affiche in new_affiche:
        if affiche_exists(affiche['link']):
            continue

        save_affiche_to_db(affiche)

        try:
            await bot.send_message(
                chat_id=CHAT_ID,
                message_thread_id=RSS_TOPIC_ID,
                text=f'Новая афиша опубликована!\n\n**{affiche["title"]}**\n{affiche["description"]}\n[Ссылка на афишу]({affiche["link"]})',
                parse_mode='MARKDOWN',
            )
        except Exception as e:
            logger.error(f'❌ Ошибка при отправке сообщения: {e}')

    logger.info('ⓘ Завершена отправка новых афиш с livefans.jp.')
