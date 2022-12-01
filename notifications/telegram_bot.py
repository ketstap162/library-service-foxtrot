import requests

from library_service import settings

TELEGRAM_API = "https://api.telegram.org/"
BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
BOT_SLUG = f"bot{BOT_TOKEN}/"
CHAT_ID = settings.TELEGRAM_CHAT_ID


class TelegramBot:
    CONTACT = TELEGRAM_API + BOT_SLUG

    @classmethod
    def send_message(cls, message):
        function = "sendMessage"

        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        print(requests.get(cls.CONTACT + function, params=payload))


if __name__ == "__main__":
    print(TelegramBot.CONTACT)
    TelegramBot.send_message("Test massage")
