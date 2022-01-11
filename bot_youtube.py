# import argparse
from os import system
import time
import sys
import json
from typing import List

import requests
from googleapiclient.discovery import build
from pytube import YouTube

from g_api import google_api_key
from tg_token import BOT_TOKEN
import re

tg_url = "https://api.telegram.org/bot"
yt_url = "https://www.youtube.com/watch?v="
offset = 0
DEVELOPER_KEY = google_api_key
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# TODO: make upload function
class InlineKeyboardButton:
    def __init__(self, i_text: str, callback_data: str = None):
        self.text = i_text
        self.callback_data = callback_data
        print("inline keyboard button triggered")

class InlineKeyboardMarkup:
    def __init__(self, i_text: str, callback_data: str = None):
        self.inline_keyboard = [[InlineKeyboardButton(i_text, callback_data)]]
        print("inline keyboard markup triggered")
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

def sendMessage(i_text, i_chat_id, link_yt="", reply_markup: List = None):
    method = "/sendMessage?"
    print(i_chat_id)
    if not reply_markup:
        if i_text == "/start":
            tg_send_message = requests.post(
                url=tg_url + BOT_TOKEN + method,
                json={
                    "chat_id": i_chat_id,
                    "text": i_text
                }
            )
        else:
            tg_send_message = requests.post(
                url=tg_url + BOT_TOKEN + method,
                json={
                    "chat_id": i_chat_id,
                    "parse_mode": "HTML",
                    "text": i_text + F"<a href=\"{link_yt}\">\nСсылка</a>"
                }
            )
            print(i_chat_id)
            print(tg_send_message.json())
    else:
        try:
            tg_send_message = requests.post(
                url=tg_url + BOT_TOKEN + method,
                json={
                    "chat_id": i_chat_id,
                    "parse_mode": "HTML",
                    "text": i_text,
                    "reply_markup": {"inline_keyboard": [reply_markup]}
                    # "reply_markup": {"inline_keyboard": [[{"text": "Button1", "callback_data": "first_1"},{"text": "Button2", "callback_data": "second_2"}]]}
                }
            )
            print(i_chat_id)
            print(tg_send_message.json())
        except:
            tg_send_message = requests.post(
                url=tg_url + BOT_TOKEN + method,
                json={
                    "chat_id": i_chat_id,
                    "text": "Что-то пошло не так, попробуйте еще раз."
                }
            )
            print(i_chat_id)
            print(tg_send_message.json())


def getUpdates():
    global offset
    method = "/getUpdates?"
    tg_request_update = requests.post(
        url=tg_url + BOT_TOKEN + method,
        json={
            "offset": offset,
            "allowed_updates": ["message", "callback_query"]
        }
    )
    message = tg_request_update.json()
    try:
        offset = int(message["result"][0]["update_id"]) + 1
    except IndexError:
        offset = 1
    print(offset)
    print(message)
    try:
        print("____________")
        # if not message["result"][0]["callback_query"]:
        if not message.get("reply_markup"):
            try:
                print("No reply markup, passing to search")
                youtubeSearch(message["result"][0]["message"]["text"],
                            message["result"][0]["message"]["chat"]["id"])
            except:
                pass
        else:
            ytAudioDownload(url_yt=yt_url+message["reply_markup"]["inline_keyboard"][0][0]["callback_data"])
    except:
        pass

def youtubeSearch(options, i_chat_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options,
        part='id,snippet',
        maxResults=5,
        type='video'
    ).execute()

    video_titles = []
    video_ids = []
    linked_text = []
    keyboard_markup = []
    # TODO: refactor loops, create separate functions(?)
    i = 1
    j = 0
    print("searching...\n___________")
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_titles.append('%s.%s' % (i, search_result['snippet']['title']))
            video_ids.append('%s' % (search_result['id']['videoId']))
            print(search_result['snippet']['title'], i_chat_id)
            keyboard_markup.append(InlineKeyboardButton(i_text=i, callback_data=search_result['id']['videoId']).__dict__)
            i = i + 1
    # TODO: add 5 buttons in a row with 1-5 numbers
    for titels in video_titles:
        linked_text.append(F'{titels} <a href=\"{yt_url+video_ids[j]}\">\nСсылка</a>')
        j = j + 1
    
    sendMessage(i_text='\n'.join(map(str, linked_text)), i_chat_id=i_chat_id, reply_markup=keyboard_markup)

def ytAudioDownload(url_yt):
    yt = YouTube(url_yt)
    yt_stream = yt.streams.get_audio_only()
    yt_stream.download()

    print(yt_stream)

if __name__ == "__main__":
    while True:
    #     getUpdates()
    #     time.sleep(1)
        print("Next? y to continue:")
        if input() != "y":
            print("Exited")
            sys.exit()
        else:
            print("Next update")
            getUpdates()