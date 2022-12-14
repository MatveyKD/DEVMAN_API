import requests
import time
import os

import telegram
from dotenv import load_dotenv

import logging


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=tg_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


if __name__ == "__main__":
    load_dotenv()

    bot = telegram.Bot(token=os.getenv("TG_BOT_TOKEN"))

    timestamp = None

    tg_handler = TelegramLogsHandler(os.getenv("TG_SERVICE_BOT_TOKEN"), os.getenv("TG_USER_ID"))

    logger = logging.getLogger("logger")
    logger.setLevel(logging.WARNING)
    logger.addHandler(tg_handler)
    
    while True:
        url = "https://dvmn.org/api/long_polling/"
        headers = {
            "Authorization": f"Token {os.getenv('DEVMAN_API_TOKEN')}"
        }
        payload = {
            "timestamp": timestamp
        }
        try:
            response = requests.get(
                url=url,
                headers=headers,
                params=payload,
                timeout=91
            )
            response.raise_for_status()
        except requests.exceptions.ReadTimeout as error:
            logger.warning(f"Timeout error: {error}")
            continue
        except requests.exceptions.ConnectionError as error:
            logger.warning(f"Connection error: {error}")
            time.sleep(10)
            continue
        reviews_info = response.json()
        if reviews_info["status"] == "timeout":
            timestamp = reviews_info["timestamp_to_request"]
        else:
            timestamp = reviews_info["last_attempt_timestamp"]
            for attempt in reviews_info["new_attempts"]:
                if attempt["is_negative"]:
                    result = "К сожалению, в работе нашлись ошибки."
                else:
                    result = "Предподавателю все понравилось, можно приступать следующему уроку!"
                bot.send_message(
                    text=f'У вас провели работу "{attempt["lesson_title"]}" {attempt["lesson_url"]}\n\n{result}',
                    chat_id=os.getenv("TG_USER_ID")
                )
