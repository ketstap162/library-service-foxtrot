import requests


BOT_TOKEN = "5940358054:AAEFRx8od9PwXF1aSRet74wy4eh1Lre0wMM"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_message(message):

    params = {
        "chat_id": "-1001542349853",
        "text": message
    }

    print(requests.get(TELEGRAM_API, params=params))


if __name__ == "__main__":
    send_message("Hello pussy")
