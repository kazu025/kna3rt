import os
from flask import Flask, request, abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from collections.abc import MutableMapping
import pya3rt
import requests

app = Flask(__name__)
line_bot_api = LineBotApi("nzU3ztIXy8kQUhovrfGXBCWdtpk4eaC8U3r2Q8N7yiD3LS9LQfKL0iKGpZWyI+/y5FXmHoOF7UWaspNBnwU0ybb1+5R6iRw374jqM7GFrVhrHBj/vIzFH3KaGzAHMIWqHqNf4igzkrqp1/C2s8acrAdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("77a039ed3c151c4f6bcfcdaf6ef68c7a")

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    ai_message=talk_ai(event.message.text)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ai_message))

def talk_ai(word):
    query_msg = word
    files = {
        'apikey': (None, 'DZZkxagPpnoQIEaCgvBE39C5oPVhdsdc'),
        'query': (None, query_msg.encode('utf-8')),
    }
    response = requests.post('https://api.a3rt.recruit.co.jp/talk/v1/smalltalk', files=files)
    res = response.json()
    try:
        ret = res['results'][0]['reply']
    except:
        ret = "内部でエラー発生しました。"
    return ret

if __name__ == '__main__':
    app.run()
    