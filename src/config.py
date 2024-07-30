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
