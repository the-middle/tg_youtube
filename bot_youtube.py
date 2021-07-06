# import argparse
import time

import requests
from googleapiclient.discovery import build
from pytube import YouTube

from g_api import google_api_key
from tg_token import BOT_TOKEN
import re

tg_url = "https://api.telegram.org/bot"
offset = 0
DEVELOPER_KEY = google_api_key
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def InlineKeybouardButton (text: str, callback_data: str = None):
    button = {
        "text": text,
        "callback_data": callback_data,
    }
    buttons = [[button]]
    return buttons

def sendMessage(i_text, i_chat_id, link_yt="", reply_markup = None):
    method = "/sendMessage?"
    print(i_chat_id)
    if reply_markup == None:
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
                    "text": i_text + F"<a href=\"{link_yt}\">\nСсылка</a>",
                    "reply_markup": reply_markup
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
    offset = int(message["result"][0]["update_id"]) + 1
    print(offset)
    print(tg_request_update.json())
    if message["result"][0]["callback_query"] == None:
        try:
            youtubeSearch(message["result"][0]["message"]["text"],
                        message["result"][0]["message"]["chat"]["id"])
        except:
            pass
    else:
        ytAudioDownload

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

    keyboard = [[InlineKeyboardButton("Hackerearth", callback_data='HElist8')]]

    videos = []
    yt_url = "https://www.youtube.com/watch?v="

    i = 0

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s (%s)' % (search_result['snippet']['title'],
                                       search_result['id']['videoId']))
            sendMessage(search_result['snippet']['title'], i_chat_id,
                        yt_url + search_result['id']['videoId'], InlineKeyboardMarkup([[InlineKeyboardButton(text=i), callback_data=search_result['id']['videoId']]]))
            print(search_result['snippet']['title'], i_chat_id)
            ytAudioDownload(yt_url + search_result['id']['videoId'])
            i = i+1

def ytAudioDownload(url_yt):
    yt = YouTube(url_yt)
    yt_stream = yt.streams.get_audio_only()
    yt_stream.download()

    print(yt_stream)

if __name__ == "__main__":
    while True:
        getUpdates()
        time.sleep(5)
