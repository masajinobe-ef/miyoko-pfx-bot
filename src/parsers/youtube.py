"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

import time
import asyncio
import yaml
import os

# Loguru
from logger import logger

# Google
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Конфигурация
from config import YOUTUBE_API_KEY


# Инициализация YouTube API
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

with open('configs/yt-channels.yaml', 'r') as file:
    channels_config = yaml.safe_load(file)

LAST_VIDEOS_FILE = 'temp/last_videos.yaml'


# Функция для загрузки последних идентификаторов видео из файла
def load_last_videos():
    try:
        if os.path.exists(LAST_VIDEOS_FILE):
            with open(LAST_VIDEOS_FILE, 'r') as file:
                return yaml.safe_load(file) or {
                    channel: None for channel in channels_config['channels']
                }
        else:
            return {channel: None for channel in channels_config['channels']}

    except Exception as e:
        logger.warning(f'Не удалось загрузить последние видео из файла: {e}')
        return {channel: None for channel in channels_config['channels']}


# Функция для сохранения временной метки последнего видео
def save_last_videos(last_videos):
    try:
        with open(LAST_VIDEOS_FILE, 'w') as file:
            yaml.safe_dump(last_videos, file)

    except Exception as e:
        logger.error(f'Ошибка при сохранении последних видео в файл: {e}')


# Загрузите последние идентификаторы видео
last_videos = load_last_videos()


MAX_QUOTA_RETRIES = 3
QUOTA_RETRY_DELAY = 60  # Задержка в секундах перед повторной попыткой


async def check_new_videos(bot, chat_id, rss_topic_id):
    try:
        quota_retries = 0
        while True:
            for channel_id in channels_config['channels']:
                try:
                    search_request = youtube.search().list(
                        part='snippet',
                        channelId=channel_id,
                        order='date',
                        maxResults=1,
                    )
                    search_response = search_request.execute()
                    latest_video = search_response['items'][0]

                    video_id = latest_video['id']['videoId']
                    video_title = latest_video['snippet']['title']
                    video_url = f'https://www.youtube.com/watch?v={video_id}'
                    video_published_at = latest_video['snippet']['publishedAt']

                    current_time = time.time()
                    video_published_time = time.mktime(
                        time.strptime(video_published_at, '%Y-%m-%dT%H:%M:%SZ')
                    )

                    if (
                        current_time - video_published_time
                    ) > 7 * 24 * 60 * 60:
                        continue  # Пропустить отправку старого видео

                    if last_videos.get(channel_id) == video_id:
                        continue  # Пропустить повторную отправку того же видео

                    last_videos[channel_id] = video_id
                    await bot.send_message(
                        chat_id=chat_id,
                        message_thread_id=rss_topic_id,
                        text=f'Новое видео опубликовано!\n\n{video_title}\n\n{video_url}',
                    )
                    save_last_videos(last_videos)

                except HttpError as http_err:
                    if (
                        'quota' in str(http_err).lower()
                        and quota_retries < MAX_QUOTA_RETRIES
                    ):
                        logger.warning(
                            'Достигнут лимит квоты YouTube API. Повторная попытка через некоторое время.'
                        )
                        quota_retries += 1
                        await asyncio.sleep(QUOTA_RETRY_DELAY)
                        continue
                    else:
                        logger.error(
                            f'🚫 HTTP ошибка при запросе к YouTube API: {http_err}'
                        )
                except Exception as err:
                    logger.error(f'🚫 Ошибка при обработке данных: {err}')

            await asyncio.sleep(60)

    except Exception as e:
        logger.warning(
            f'🚫 Общая ошибка в цикле проверки новых видео Youtube: {e}'
        )
