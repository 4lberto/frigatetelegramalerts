import asyncio
import json
import logging
import shutil
import uuid
from time import sleep
from typing import Dict

import requests

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
import telegram

logging.basicConfig(level=logging.INFO)

frigate_basic_auth_user = "USER"
frigate_basic_auth_password = "PASSWORD"
frigate_base_url = "https://my_home_frigate_url:port"

telegram_chat_id = "-123456789"
telegram_bot_token = "093458609587094:lisñoisfgpoi098w3ñohiañnfg"

bot = telegram.Bot(token=telegram_bot_token)
sleep_time_in_secs = 5


def get_latest_event():
    base_url = f"{frigate_base_url}/api/events?cameras=all&labels=all&zones=all&sub_labels=all&favorites=0&include_thumbnails=0&limit=5"

    http_respose = requests.get(base_url, verify=False, auth=(frigate_basic_auth_user, frigate_basic_auth_password))
    result = json.loads(http_respose.text)
    # print(json.dumps(result, indent=4))
    if result:
        return result[0]
    return None


async def notify_telegram(event: dict):
    event_id = event.get("id")
    img_base_url = f"{frigate_base_url}/api/events/{event_id}/thumbnail.jpg"
    print("---- notify_telegram -----")
    print(img_base_url)
    image_full_path = __download_photo(img_base_url)
    print(json.dumps(event, indent=4))
    await bot.send_message(chat_id=telegram_chat_id,
                           text=f"{event['label']} en {event['camera']} ({event['top_score']}%) - {img_base_url}")
    await bot.send_photo(chat_id=telegram_chat_id, photo=open(image_full_path, 'rb'))


def __download_photo(img_url: str) -> str:
    response = requests.get(img_url, stream=True, verify=False,
                            auth=(frigate_basic_auth_user, frigate_basic_auth_password))
    image_temp_name = uuid.uuid4().hex

    base_path = "/tmp"
    full_path = f"{base_path}/{image_temp_name}.jpg"

    with open(full_path, 'wb') as fout:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, fout)
    return full_path


if __name__ == '__main__':
    notified_events = set()
    while (True):
        latest_event: Dict = get_latest_event()
        if latest_event is not None:
            if latest_event["id"] not in notified_events:
                asyncio.run(notify_telegram(latest_event))
                notified_events.add(latest_event["id"])

        sleep(sleep_time_in_secs)
