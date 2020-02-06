#%%
import math
from pickle import load
from pathlib import Path
from random import choice
from linebot.models import *


class Bot:
    def __init__(self):
        self.restaurants = self.load_restaurants()
        self.jpg_urls = self.load_jpgs()

    def load_restaurants(self, fname="restaurants.pickle"):
        with open(fname, "rb") as file:
            restaurants = load(file)
        for i in range(len(restaurants)):
            restaurants[i]["idx"] = i
        return restaurants

    def load_jpgs(self, path="nccueater"):
        jpg_fnames = [str(fname) for fname in Path(path).glob("*.jpg")]
        base_url = "https://nccu-gourmet-line-bot.appspot.com/"
        jpg_urls = [base_url + fname for fname in jpg_fnames]
        return jpg_urls

    def get_img(self):
        img_path = choice(self.jpg_urls)
        img_message = ImageSendMessage(
            original_content_url=img_path, preview_image_url=img_path
        )
        return img_message

    def get_restaurant(self):
        restaurant = choice(self.restaurants)
        if "formatted_address" in restaurant:
            address = restaurant["formatted_address"]
        else:
            address = restaurant["vicinity"]
        loc_message = LocationSendMessage(
            title=restaurant["name"],
            address=address,
            latitude=restaurant["geometry"]["location"]["lat"],
            longitude=restaurant["geometry"]["location"]["lng"],
        )
        return loc_message

    def list_restaurants(self, idx=-1):
        text = ""
        if idx > 0:
            total_page = math.ceil(len(self.restaurants) / 10)
            text += f"第{idx}頁/共{total_page}頁\n"
            for restaurant in self.restaurants[(idx - 1) * 10 : idx * 10]:
                text += f"{restaurant['idx']}: {restaurant['name']}\n"
        else:
            for restaurant in self.restaurants:
                text += f"{restaurant['idx']}: {restaurant['name']}\n"
        txt_message = TextSendMessage(text=text[:-1])
        return txt_message

    def help_menu(self):
        text = [
            "指令表:\n",
            "吃 → 隨機選擇一間餐廳\n",
            "喝 → 隨機選擇一種飲料\n",
            "抽 → 從吃貨政大IG隨機抽一張圖片\n",
            "餐廳 → 列出所有餐廳",
        ]
        txt_message = TextSendMessage(text="".join(text))
        return txt_message

    def handle_message(self, in_msg):
        out_msg = TextSendMessage(text="")
        if in_msg == "help":
            out_msg = self.help_menu()
        if in_msg[0] == "吃":
            if len(in_msg) == 1:
                out_msg = self.get_restaurant()
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
            out_msg = self.get_img()
        elif in_msg[0:2] == "餐廳":
            if in_msg[2:3].isdigit():
                out_msg = self.list_restaurants(eval(in_msg[2]))
            else:
                out_msg = self.list_restaurants()
        return out_msg


# %%
if __name__ == "__main__":
    bot = Bot()
    out = bot.handle_message("help")
    print(out)

# %%
