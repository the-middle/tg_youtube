from token import BOT_TOKEN
import requests

def getUpdates():
    tg_url = "https://api.telegram.org/bot"
    method = "/getUpdates?"
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

