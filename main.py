import requests
import time
import os

import telegram
from dotenv import load_dotenv

import logging


if __name__ == "__main__":
    load_dotenv()

    bot = telegram.Bot(token=os.getenv("TG_BOT_TOKEN"))

    timestamp = None
    
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
            logging.warning(f"Timeout error: {error}")
        except requests.exceptions.ConnectionErro as error:
            logging.warning(f"Timeout error: {error}")
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
