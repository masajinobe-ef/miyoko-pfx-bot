"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

import yaml


with open('configs/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Bot
API_TOKEN = config['bot']['token']
CHAT_ID = config['bot']['chat_id']
TOPIC_ID = int(config['bot']['topic_id'])
RSS_TOPIC_ID = int(config['bot']['rss_topic_id'])

# Youtube
YOUTUBE_API_KEY = config['youtube']['api_key']

# VK
VK_API_TOKEN = config['vk']['api_token']
VK_API_VERSION = config['vk']['api_version']

with open('configs/vk-domains.yaml', 'r') as file:
    domains_config = yaml.safe_load(file)

DOMAINS = domains_config['domains']
