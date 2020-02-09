#%%
import math
from pickle import load
from pathlib import Path
from random import choice
from linebot.models import *


class Bot:
    def __init__(self):
        self.foods = self.load_file("foods.pickle")
        self.drinks = self.load_file("drinks.pickle")
        self.keyword_id = self.load_file("keyword_id.pickle")
        self.id_index = self.load_file("id_index.pickle")
        self.all = self.load_file("all.pickle")
        self.jpg_urls = self.load_jpgs()
        self.rice_keywords = ["飯", "rice", "炒飯", "自助餐", "燉飯", "risotto", "飯館", "合菜"]
        self.noodle_keywords = ["麵", "noodle", "炒麵", "湯麵"]
        self.rice_restaurants = self.get_restaurants_by_keywords(self.rice_keywords)
        self.noodle_restaurants = self.get_restaurants_by_keywords(self.noodle_keywords)

    def get_restaurants_by_keywords(self, keywords):
        restaurants = []
        place_ids = []
        for keyword in keywords:
            place_ids += self.keyword_id[keyword]
        for place_id in set(place_ids):
            index = self.id_index[place_id]
            restaurant = self.all[index]
            restaurants.append(restaurant)
        return restaurants

    def load_file(self, fname="foods.pickle"):
        with open(fname, "rb") as file:
            restaurants = load(file)
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

    def get_restaurant(self, place_type="foods"):
        if place_type == "foods":
            restaurants = self.foods
        elif place_type == "drinks":
            restaurants = self.drinks
        elif place_type == "rice":
            restaurants = self.rice_restaurants
        elif place_type == "noodle":
            restaurants = self.noodle_restaurants

        restaurant = choice(restaurants)
        if "formatted_address" in restaurant:
            address = restaurant["formatted_address"]
        else:
            address = restaurant["vicinity"]
        restaurant_id = restaurant["index"]
        loc_message = LocationSendMessage(
            title=f"{restaurant['index']}: {restaurant['name']}",
            address=address,
            latitude=restaurant["geometry"]["location"]["lat"],
            longitude=restaurant["geometry"]["location"]["lng"],
        )
        txt_message = TextSendMessage(f'Google評價: {restaurant["rating"]}')
        return [loc_message, txt_message]

    def list_restaurants(self, place_type="foods", idx=-1):
        if place_type == "foods":
            restaurants = self.foods
        elif place_type == "drinks":
            restaurants = self.drinks

        text = ""
        if idx > 0:
            total_page = math.ceil(len(restaurants) / 10)
            text += f"第{idx}頁/共{total_page}頁\n"
            for restaurant in restaurants[(idx - 1) * 10 : idx * 10]:
                text += f"{restaurant['idx']}: {restaurant['name']}\n"
        else:
            for restaurant in restaurants:
                text += f"{restaurant['idx']}: {restaurant['name']}\n"
        txt_message = TextSendMessage(text=text[:-1])
        return txt_message

    def help_menu(self):
        text = [
            "指令表:\n",
            "吃 → 隨機選擇一間餐廳\n",
            "喝 → 隨機選擇一種飲料\n",
            "抽 → 從吃貨政大IG隨機抽一張圖片\n",
            "餐廳 → 列出所有餐廳\n",
            "關於 → 顯示小助手的相關資訊",
        ]
        txt_message = TextSendMessage(text="".join(text))
        return txt_message

    def about_msg(self):
        text = ["開發者: PM\n", "版本: v1.0\n", "更新時間: 2019/2/9"]
        txt_message = TextSendMessage(text="".join(text))
        return txt_message

    def handle_message(self, in_msg):
        out_msg = TextSendMessage(text="")
        if in_msg == "help":
            out_msg = self.help_menu()
        if in_msg[0] == "吃":
            if len(in_msg) == 1:
                out_msg = self.get_restaurant("foods")
            else:
                if in_msg[1] == "飯":
                    out_msg = self.get_restaurant("rice")
                elif in_msg[1] == "麵":
                    out_msg = self.get_restaurant("noodle")
                elif in_msg[1] == "素":
                    pass
                elif in_msg[1:3] == "點心":
                    pass
                elif in_msg[1] == "貨":
                    pass
        elif in_msg[0] == "喝":
            if (len(in_msg)) == 1:
                out_msg = self.get_restaurant("drinks")
            else:
                if in_msg[1] == "茶":
                    pass
                elif in_msg[1:3] == "咖啡":
                    pass
                else:
                    pass
        elif in_msg[0] == "抽":
            out_msg = self.get_img()
        elif in_msg[0:2] == "餐廳":
            if in_msg[2:].isdigit():
                out_msg = self.list_restaurants("foods", eval(in_msg[2]))
            else:
                out_msg = self.list_restaurants("foods")
        elif in_msg[0:3] == "飲料店":
            if in_msg[2:].isdigit():
                out_msg = self.list_restaurants("drinks", eval(in_msg[2]))
            else:
                out_msg = self.list_restaurants("drinks")
        elif in_msg == "關於":
            out_msg = self.about_msg()
        return out_msg


# %%
if __name__ == "__main__":
    bot = Bot()
    out = bot.handle_message("吃飯")
    print(out)

# %%
