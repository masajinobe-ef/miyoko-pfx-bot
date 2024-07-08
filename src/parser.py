"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

import asyncio
import yaml
import os

# Google
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Loguru
from logger import logger


# Config file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# YouTube channels
with open('yt-channels.yaml', 'r') as file:
    channels_config = yaml.safe_load(file)

# Initialize YouTube API
YOUTUBE_API_KEY = config['youtube']['api_key']
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


# File to store the last video IDs
LAST_VIDEOS_FILE = 'last_videos.yaml'


# Function to load the last video IDs from file
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


# Function to save the last video IDs to file
def save_last_videos(last_videos):
    try:
        with open(LAST_VIDEOS_FILE, 'w') as file:
            yaml.safe_dump(last_videos, file)
    except Exception as e:
        logger.error(f'Ошибка при сохранении последних видео в файл: {e}')


# Load last video IDs
last_videos = load_last_videos()


async def check_new_videos(bot, chat_id):
    try:
        while True:
            for channel_id in channels_config['channels']:
                try:
                    # Fetch channel title
                    channel_request = youtube.channels().list(
                        part='snippet',
                        id=channel_id,
                    )
                    channel_response = channel_request.execute()
                    channel_title = channel_response['items'][0]['snippet'][
                        'title'
                    ]

                    # Fetch latest video
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

                    if last_videos[channel_id] != video_id:
                        last_videos[channel_id] = video_id
                        await bot.send_message(
                            chat_id=chat_id,
                            text=f'Новое видео с канала {channel_title} опубликовано!\n\n{video_title}\n\n{video_url}',
                        )
                        save_last_videos(last_videos)

                except HttpError as http_err:
                    logger.error(
                        f'HTTP ошибка при запросе к YouTube API: {http_err}'
                    )
                except Exception as err:
                    logger.error(f'Ошибка при обработке данных: {err}')

            await asyncio.sleep(60)

    except Exception as e:
        logger.warning(f'Общая ошибка в цикле проверки новых видео: {e}')
