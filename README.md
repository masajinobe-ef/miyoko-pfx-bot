# Miyoko

<img src="pic.png" alt="pic"/>

**Telegram-бот для сообщества Priscilla FX**

## Описание

Проект использует следующие библиотеки:

- **[Aiogram](https://aiogram.dev)**
- **[Loguru](https://github.com/Delgan/loguru)**
- **[Pyyaml](https://github.com/yaml/pyyaml)**
- **[Requests](https://requests.readthedocs.io/en/latest)**
- **[Google API](https://github.com/googleapis/google-api-python-client)**

### Установка

Для работы потребуется [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) и [Python](https://www.python.org/)

Клонируйте репозиторий:

```sh
git clone https://github.com/masajinobe-ef/miyoko-pfx-bot.git
```

Настройте config.yaml в папке configs:

```yaml
bot:
  token: "1234567890ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba" # Бот токен (@BotFather)
  chat_id: -1001234567890 # Чат ID. -100 префикс, если supergroup.
  topic_id: 41223 # ID основной темы в чате.
  rss_topic_id: 30421 # ID темы для рассылки.

youtube:
  api_key: "AIzaSyDF4MZIBk29FN-hs362OnuW9c-uk1IGBEg" # Google API для рассылки

vk:
  api_token: "89ba2f3b89ba2f3b89ba2f3b158aa360b8889ba89ba2f3bef2b2d32a3ed373733769e75" # Токен приложения VK
  api_version: "5.199" # Версия API
```

#### License

**This project is licensed under the GPL-3.0 license.**
