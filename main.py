import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, abort, send_from_directory
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from backend import Bot

# Load TOKEN & KEY from .env
load_dotenv(find_dotenv())
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
SECRET_KEY = os.environ.get("SECRET_KEY")

# Setup Line API
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET_KEY)

# Init Backend Line bot
bot = Bot()

# Flask APP
app = Flask(__name__)


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


# Handling Incoming Message
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        msg = event.message.text
        msg = bot.handle_message(msg)
        line_bot_api.reply_message(event.reply_token, msg)


@app.route("/nccueater/<path:fname>")
def get_img(fname):
    return send_from_directory("nccueater", fname)


# Start from here!
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
