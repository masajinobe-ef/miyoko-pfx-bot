"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

import asyncio
import re
from datetime import datetime, timezone

import requests
import yaml
# Aiogram
from aiogram import Router

# Config
from config import VK_API_TOKEN, VK_API_VERSION
# Loguru
from logger import logger

router = Router()


# Check new posts
@router.message()
async def check_new_posts(bot, domains, chat_id, rss_topic_id):
    try:
        sent_posts = set()
        last_run_timestamp = datetime.now(timezone.utc)
        while True:
            for domain in domains:
                response = requests.get(
                    'https://api.vk.com/method/wall.get',
                    params={
                        'access_token': VK_API_TOKEN,
                        'domain': domain,
                        'count': 1,
                        'v': VK_API_VERSION,
                        'filter': 'all',
                    },
                )
                if response.status_code == 200:
                    data = response.json().get('response', {}).get('items', [])
                    if data:
                        post = data[0]
                        post_id = post.get('id')
                        post_key = f'{domain}_{post_id}'
                        if post_key in sent_posts:
                            continue  # Пропустить отправку, если сообщение уже отправлено
                        if post.get('is_pinned'):
                            continue  # Пропустить отправку закрепленных сообщений
                        post_date = datetime.fromtimestamp(
                            post.get('date'), tz=timezone.utc
                        )
                        if post_date < last_run_timestamp:
                            continue  # Пропустить отправку постов, созданных во время простоя
                        text = post.get('text', '')
                        group_url = f'https://vk.com/{domain}'
                        post_url = f'https://vk.com/{domain}?w=wall{post.get("owner_id")}_{post_id}'
                        text = re.sub(
                            r'https?://\S+',
                            f'[ссылка]({post_url})',
                            text,
                        )
                        formatted_text = f'Источник: [{domain}]({group_url})\n\n\n{text}\n\n[Ссылка на пост]({post_url})'
                        await bot.send_message(
                            chat_id=chat_id,
                            message_thread_id=rss_topic_id,
                            text=formatted_text,
                            parse_mode='Markdown',
                        )
                        sent_posts.add(post_key)
                        with open('temp/sent_posts.yaml', 'w') as file:
                            yaml.dump(list(sent_posts), file)
                await asyncio.sleep(30)

    except Exception as e:
        logger.warning(
            f'🚫 Общая ошибка в проверке цикла на новые посты VK: {e}'
        )
