"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

import os
import asyncio
from datetime import datetime, timedelta

import pytz
import aiohttp

# Web
from bs4 import BeautifulSoup

# Loguru
from loguru import logger

# Config
from config import CHAT_ID, RSS_TOPIC_ID

# Database
from database import init_db, session

# Models
from models import LiveFansAffiche, LiveFansURLs


# Get URLs from Database
def get_all_urls():
    try:
        urls = session.query(LiveFansURLs.url).all()
        return [url[0] for url in urls]
    except Exception as e:
        logger.error(f'❌ Ошибка при получении URL из базы данных: {e}')
        return []
    finally:
        session.close()


async def livefans_affiche(bot):
    if not os.path.exists('database.db'):
        init_db()
        logger.info(
            'ℹ️ База данных инициализирована впервые. Начинаем проверку новых афиш с livefans.jp.'
        )
        await check_and_send_affiches(bot)
    else:
        await check_and_send_affiches(bot)
        while True:
            tokyo_tz = pytz.timezone('Asia/Tokyo')
            now = datetime.now(tokyo_tz)
            next_midnight = now.replace(
                hour=0, minute=0, second=0, microsecond=0
            ) + timedelta(days=1)
            wait_time = (next_midnight - now).total_seconds()

            logger.info(
                '⏳ Ожидание до следующей проверки афиш с livefans.jp в полночь по японскому времени.'
            )
            await asyncio.sleep(wait_time)

            await check_and_send_affiches(bot)


async def fetch_affiche(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                soup = BeautifulSoup(await response.text(), 'html.parser')

                # Получаем только первый элемент div
                element = soup.find(
                    'div', class_=['whiteBack midBox fes', 'whiteBack midBox']
                )

                affiche = []
                if element:
                    h3_tag = (
                        element.find('h3').text if element.find('h3') else None
                    )
                    img_tag = (
                        element.find('img')['src']
                        if element.find('img')
                        else None
                    )
                    p_tag = (
                        element.find('p').text if element.find('p') else None
                    )
                    a_tag = (
                        element.find('a')['href']
                        if element.find('a')
                        else None
                    )
                    full_link = (
                        f'https://www.livefans.jp{a_tag}' if a_tag else None
                    )
                    affiche.append(
                        {
                            'title': h3_tag,
                            'image': img_tag,
                            'description': p_tag,
                            'link': full_link,
                        }
                    )
                return affiche

    except aiohttp.ClientError as e:
        logger.error(f'❌ Ошибка при получении афиш с {url}: {e}')
        return []
    except Exception as e:
        logger.error(f'❌ Неизвестная ошибка при получении афиш с {url}: {e}')
        return []


async def save_affiche_to_db(affiche):
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


async def check_and_send_affiches(bot):
    urls = get_all_urls()
    last_sent_links = set()
    existing_affiches = session.query(LiveFansAffiche.link).all()
    existing_links = {affiche[0] for affiche in existing_affiches}

    for url in urls:
        new_affiche = await fetch_affiche(url)
        for affiche in new_affiche:
            if (
                affiche['link'] in existing_links
                or affiche['link'] in last_sent_links
            ):
                continue

            await save_affiche_to_db(affiche)

            last_sent_links.add(affiche['link'])

            await asyncio.sleep(2)

            while True:
                try:
                    await bot.send_message(
                        chat_id=CHAT_ID,
                        message_thread_id=RSS_TOPIC_ID,
                        text=f'ℹ️ Новая афиша опубликована!\n\n**{affiche["title"]}**\n{affiche["description"]}\n[Ссылка на афишу]({affiche["link"]})',
                        parse_mode='MARKDOWN',
                    )
                    logger.info(
                        f'✅ Сообщение c афишей отправлено: {affiche["link"]}'
                    )
                    break

                except Exception as e:
                    logger.error(f'❌ Ошибка при отправке сообщения: {e}')
                    if 'Flood control exceeded' in str(e):
                        wait_time = int(e.description.split('retry after ')[1])
                        logger.info(
                            f'⏳ Ожидание {wait_time} секунд перед повторной попыткой отправки сообщения.'
                        )
                        await asyncio.sleep(wait_time)  # Ждем указанное время
                    else:
                        break  # Если ошибка не связана с ограничениями, выходим из цикла

    logger.info('✅ Завершена отправка новых афиш.')
