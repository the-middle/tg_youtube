# import argparse
import io
import subprocess
from concurrent.futures import process
import json
import os
import sys
import time
from io import BytesIO
from turtle import st
from typing import List, Text

import requests
from googleapiclient.discovery import build
from pydub import AudioSegment
from pytube import YouTube

from g_api import google_api_key
from tg_token import BOT_TOKEN

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
    print(F"Chat id inside sendMessage: {i_chat_id}")
    print(F"Text message: {i_text}")
    if not reply_markup:
        if i_text == "/start":
            print("Inside")
            tg_send_message = requests.post(
                url=tg_url + BOT_TOKEN + method,
                json={
                    "chat_id": i_chat_id,
                    "parse_mode": "Markdown",
                    "text": "*Как работает бот:*\nБот получает от тебя название песни, ищет её на YouTube и предлагает на выбор первые 5 песен из результатов поиска. После клика по кнопке с нужным номером необходимо подождать несколько секунд и получить свою песню."
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
    if bool(message.get("result")):
        try:
            offset = int(message["result"][0]["update_id"]) + 1
        except IndexError:
            offset = 1
        print(offset)
        print(message)
        try:
            print("____________")
            print(bool(message.get("result")))
            print(message.get("result"))
            print("------------")
            print(message.get("result")[0].get("callback_query"))
            if message.get("result")[0].get("callback_query") is None:
                print("Inside if")
                if message.get("result")[0].get("message").get("text") == "/start":
                    print("Sending message")
                    sendMessage(i_text=message.get("result")[0].get("message").get("text"), i_chat_id=message.get("result")[0].get("message").get("chat").get("id"))
                else:
                    try:
                        print("No reply markup, passing to search")
                        youtubeSearch(message["result"][0]["message"]["text"],
                                    message["result"][0]["message"]["chat"]["id"])
                    except:
                        pass
            else:
                print("-------------------")
                print(message.get("result")[0].get("callback_query").get("data"))
                audio_stream = ytAudio(url_yt=yt_url+message.get("result")[0].get("callback_query").get("data"))
                # audio_stream = ytAudio(url_yt=yt_url+message["reply_markup"]["inline_keyboard"][0][0]["callback_data"])
                sendAudio(i_chat_id=message.get("result")[0].get("callback_query").get("from").get("id"), audio=audio_stream[0], duration=audio_stream[1], title=audio_stream[2])
        except:
            pass

def youtubeSearch(options: str, i_chat_id: str):
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
    for titels in video_titles:
        linked_text.append(F'{titels} <a href=\"{yt_url+video_ids[j]}\">\nСсылка</a>')
        j = j + 1
    
    sendMessage(i_text='\n'.join(map(str, linked_text)), i_chat_id=i_chat_id, reply_markup=keyboard_markup)

def ytAudio(url_yt: str):
    audio = BytesIO()
    yt = YouTube(url_yt)
    print(yt.streams.all())
    yt_stream = yt.streams.filter(type="audio", subtype="webm", audio_codec="opus").order_by("abr").last()
    print(yt_stream)
    yt_stream.stream_to_buffer(audio)
    print("---------------")
    print(F'Audio lenght: {yt.length}')
    print(F'Title: {yt.title}')
    audio.seek(0)
    command = ['ffmpeg', '-y', '-i', '-', '-q:a', '3', '-f', 'mp3', '-']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # mp3_audio = AudioSegment.from_file(file=audio.seek(0),format="webm",codec="opus")
    # mp3_audio_raw = BytesIO(audio.read())
    mp3_audio, errordata = process.communicate(audio.read())
    return [mp3_audio, yt.length, yt.title]

def sendAudio(i_chat_id: str, audio: bytes, duration: str, title: str):
    method = "/sendAudio?"
    # chat_id = F"chat_id={i_chat_id}?"
    tg_send_message = requests.post(
        url=tg_url + BOT_TOKEN + method,
        # json={
        #     "chat_id": i_chat_id,
        #     "video": audio,
        #     "duration": duration,
        #     "width": "1920",
        #     "height": "1080"
        # },
        data={
            "chat_id": i_chat_id,
            "duration": duration,
            # "video": audio
        },
        files={'audio': (title, audio, "audio/mp3")}
    )
    print(F'Duration: {duration}')
    print(F'Chat id: {i_chat_id}')
    print(tg_send_message.json())

if __name__ == "__main__":
    while True:
        getUpdates()
        time.sleep(1)
        # print("Next? y to continue:")
        # if input() != "y":
        #     print("Exited")
        #     sys.exit()
        # else:
        #     print("Next update")
        #     getUpdates()
