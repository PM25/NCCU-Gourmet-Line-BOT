from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = Flask(__name__)

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
SECRET_KEY = os.environ.get("SECRET_KEY")

# Channel Access Token
line_bot_api = LineBotApi(ACCESS_TOKEN)
# Channel Secret
handler = WebhookHandler(SECRET_KEY)


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
from random import randint
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if(event.source.user_id != 'Udeadbeefdeadbeefdeadbeefdeadbeef'):
        msg = event.message.text
        # msg = msg.encode('utf-8')
        if(msg == '吃'):
           msg = str(randint(1, 100))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
