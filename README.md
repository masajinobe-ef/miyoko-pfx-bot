# Miyoko

<img src="pic.png" alt="pic"/>

**Telegram-бот для сообщества Priscilla FX**

### Установка

Для работы потребуется [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) и [Python](https://www.python.org)

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
```

#### License

**This project is licensed under the GPL-3.0 license.**
