import os

import requests


TELEGRAM_API = "https://api.telegram.org/"
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_SLUG = f"bot{BOT_TOKEN}/"
CHAT_ID = os.getenv("CHAT_ID")


class TelegramBot:
    CONTACT = TELEGRAM_API + BOT_SLUG

    @classmethod
    def send_message(cls, message):
        function = "sendMessage"
        url = cls.CONTACT + function

        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        print(requests.get(url, params=payload))


if __name__ == "__main__":
    TelegramBot.send_message("Test massage")
