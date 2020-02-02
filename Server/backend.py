#%%
from pickle import load

with open("restaurants.pickle", "rb") as file:
    restaurants = load(file)

#%%
from pathlib import Path
from random import choice
from linebot.models import *


def handle_message(in_msg):
    out_msgs = TextSendMessage(text="無")
    if in_msg == "help":
        text = "吃: 隨機選擇一間餐廳\n" + "喝: 隨機選擇一種飲料"
        out_msgs = TextSendMessage(text=text)
    if in_msg[0] == "吃":
        if len(in_msg) == 1:
            out_msgs = get_restaurant()
        else:
            if in_msg[1] == "飯":
                pass
            elif in_msg[1] == "麵":
                pass
            elif in_msg[1] == "素":
                pass
            elif in_msg[1:3] == "點心":
                pass
            elif in_msg[1] == "貨":
                pass
    elif in_msg[0] == "喝":
        if in_msg[1] == "茶":
            pass
        elif in_msg[1:3] == "咖啡":
            pass
        else:
            pass
    elif in_msg[0] == "抽":
        out_msgs = ImageSendMessage(
            original_content_url=get_img(), preview_image_url=get_img()
        )
    return out_msgs


def get_img():
    fnames = [fname for fname in Path("nccueater").glob("*.jpg")]
    base_url = "https://nccu-gourmet-line-bot.appspot.com/"
    img_path = base_url + str(choice(fnames))
    return img_path


def get_restaurant():
    restaurant = choice(restaurants)
    if "formatted_address" in restaurant:
        address = restaurant["formatted_address"]
    else:
        address = restaurant["vicinity"]
    message = LocationSendMessage(
        title=restaurant["name"],
        address=address,
        latitude=restaurant["geometry"]["location"]["lat"],
        longitude=restaurant["geometry"]["location"]["lng"],
    )
    return message
