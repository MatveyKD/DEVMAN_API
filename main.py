import requests
import time
import os

import telegram
from dotenv import load_dotenv


load_dotenv()

bot = telegram.Bot(token=os.getenv("TG_BOT_TOKEN"))

timestamp = None

if __name__ == "__main__":
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
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(10)
            continue
        response_data = response.json()
        if response_data["status"] == "timeout":
            timestamp = response_data["timestamp_to_request"]
        else:
            timestamp = response_data["last_attempt_timestamp"]
            for attempt in response_data["new_attempts"]:
                if attempt["is_negative"]:
                    result = "К сожалению, в работе нашлись ошибки."
                else:
                    result = "Предподавателю все понравилось, можно приступатьк следующему уроку!"
                bot.send_message(
                    text=f'У вас провели работу "{attempt["lesson_title"]}" {attempt["lesson_url"]}\n\n{result}',
                    chat_id=os.getenv("TG_USER_ID")
                )
