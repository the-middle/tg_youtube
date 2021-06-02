from tg_token import BOT_TOKEN
import requests

# def sendMessage(text):


def getUpdates():
    tg_url = "https://api.telegram.org/bot"
    method = "/getUpdates?"
    tg_request = requests.post(
        url=tg_url + BOT_TOKEN + method
    )
    message = tg_request.json()
    # print(tg_request.text)
    print(message["result"][0]["message"]["text"])
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
    getUpdates()
