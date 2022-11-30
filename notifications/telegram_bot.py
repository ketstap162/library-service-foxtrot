import requests


TELEGRAM_API = "https://api.telegram.org/"
BOT_TOKEN = "5852038857:AAEHsZaLQOLm3bptGebQoLc9AFGe_Sa-67Q"
BOT_SLUG = f"bot{BOT_TOKEN}/"
CHAT_ID = "-1001824191547"


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
    TelegramBot.send_message("Test massage")
