"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""

import yaml

with open('configs/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Bot
API_TOKEN = config['BOT']['API_TOKEN']
PAYMENTS_TOKEN = config['BOT']['PAYMENTS_TOKEN']
CHAT_ID = config['BOT']['CHAT_ID']
TOPIC_ID = int(config['BOT']['TOPIC_ID'])
FEED_TOPIC_ID = int(config['BOT']['FEED_TOPIC_ID'])
ECHO_DB = config['BOT']['ECHO_DB'].lower() == 'true'
