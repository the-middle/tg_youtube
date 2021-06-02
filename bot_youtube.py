from tg_token import BOT_TOKEN
import requests
import time

tg_url = "https://api.telegram.org/bot"
offset = 0

def sendMessage(i_text, i_chat_id):
    method = "/sendMessage?"
    print(i_chat_id)
    if i_text == "/start":
        tg_send_message = requests.post(
            url=tg_url + BOT_TOKEN + method,
            json={
                "chat_id": i_chat_id,
                "text": i_text
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
            "offset": offset
        }
    )
    message = tg_request_update.json()
    offset = int(message["result"][0]["update_id"]) + 1
    print(offset)
    print(tg_request_update.json())
    try:
        print(message["result"][0]["message"]["text"])
        sendMessage(message["result"][0]["message"]["text"], message["result"][0]["message"]["chat"]["id"])
    except:
        pass
# def botRequest():
#     tg_url = "https://api.telegram.org/bot"
#     method = "/sendMessage?"
#     if getImg() != 'Нет фото.':
#         tg_request = requests.post(
#             url=tg_url + token + method,
#             json={
#                 "chat_id": "@wiki_shit",
#                 "parse_mode": "HTML",
#                 "text": getText() + F"<a href=\"{getImg()}\">&#8205;</a>" + F"<a href=\"{getURL()}\">\nСсылка</a>",
#                 "disable_web_page_preview": False
#             }
#         )
#     else:
#         tg_request = requests.post(
#             url=tg_url + token + method,
#             json={
#                 "chat_id": "@wiki_shit",
#                 "parse_mode": "HTML",
#                 "text": getText() + F"<a href=\"{getURL()}\">\nСсылка</a>",
#                 "disable_web_page_preview": True
#             }
#         )
#     print(tg_request.text)

if __name__ == "__main__":
    while True:
        getUpdates()
        time.sleep(5)