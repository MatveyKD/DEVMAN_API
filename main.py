import requests
import time
import os

import telegram
from dotenv import load_dotenv

import logging


logger = logging.getLogger("logger")


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=tg_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


if __name__ == "__main__":
    timestamp = None

    load_dotenv()
    tg_handler = TelegramLogsHandler(os.getenv("TG_SERVICE_BOT_TOKEN"), os.getenv("TG_USER_ID"))

    bot = telegram.Bot(token=os.getenv("TG_BOT_TOKEN"))

    logger.setLevel(logging.WARNING)
    logger.addHandler(tg_handler)

    logger.info("Bot was started")
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
                timeout=10
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            logger.warning(f'HTTPError: {error}')
        except requests.exceptions.ReadTimeout:
            logger.warning('ReadTimeout')
        except telegram.error.TimedOut:
            logging.warning("Не удалось отправить сообщение в телеграмм")
        except requests.exceptions.ConnectionError:
            logging.warning('Connection Error\nPlease check your internet connection')
        else:
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
