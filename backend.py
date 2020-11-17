#%%
import re
import math
from pickle import load
from pathlib import Path
from random import choice
from linebot.models import *
from mylib.database import Database


# line bot backend
class Bot:
    def __init__(self):
        self.food_places = None
        self.drink_places = None
        self.jpg_urls = self.load_jpgs()
        self.places_ref = Database().get_collection("places")

    # load places
    def load_places(self, mykeywords="food"):
        if mykeywords == "food":
            if self.food_places == None:
                print("*Fetch food places from database.")
                food_places = self.places_ref.where("mykeywords", "==", "food").stream()
                self.food_places = [place.to_dict() for place in food_places]
            return self.food_places
        elif mykeywords == "drink":
            if self.food_places == None:
                print("*Fetch drink places from database.")
                drink_places = self.places_ref.where(
                    "mykeywords", "==", "drink"
                ).stream()
                self.drink_places = [place.to_dict() for place in drink_places]
            return self.drink_places

    # Handle Incoming Message from Line
    def handle_message(self, msg):
        str_part = re.match(r"[\u4e00-\u9fa5a-zA-Z]*", msg).group(0)
        num_part = re.match(r"[0-9]*", msg).group(0)
        num_part = -1 if num_part == "" else eval(num_part)

        return {
            "help": lambda: self.help_menu("simple"),
            "指令": lambda: self.help_menu("all"),
            "吃": lambda: self.get_restaurant("food"),
            "喝": lambda: self.get_restaurant("drink"),
            "開": lambda: self.list_restaurants("open_now", num_part),
            "抽": lambda: self.get_img(),
            "餐廳": lambda: self.list_restaurants("food", num_part),
            "飲料店": lambda: self.list_restaurants("drink", num_part),
            "關於": lambda: self.about(),
        }.get(str_part, lambda: None)()

    # help menu
    def help_menu(self, display="simple"):
        text = [
            "簡易指令表:\n",
            "指令 → 列出所有的指令\n",
            "吃 → 隨機選擇一間餐廳\n",
            "喝 → 隨機選擇一種飲料\n",
            "開 → 列出正在營業餐廳\n",
            "抽 → 隨機抽一張餐點圖片\n",
            "關於 → 相關資訊",
        ]
        if display == "all":
            text += [
                "\n",
                "吃(飯、麵、素、點心、麵包) → 隨機選擇一間餐廳(飯、麵、素、點心、麵包)\n",
                "喝(茶、咖啡) → 隨機選擇一間飲料店(茶、咖啡)\n",
                "餐廳 → 列出所有餐廳\n",
                "餐廳(數字:n) → 顯示第n頁餐廳\n",
                "飲料店 → 列出所有飲料店\n",
                "飲料店(數字:n) → 顯示第n頁飲料店\n",
                "吃貨 → 隨機選擇一間專業美食家推薦的餐廳",
            ]
        txt_message = TextSendMessage(text="".join(text))
        return txt_message

    # randomly choose a restaurant or drink store
    def get_restaurant(self, place_type="food"):
        if place_type == "food":
            restaurants = self.load_places("food")
        elif place_type == "drink":
            restaurants = self.load_places("drink")

        restaurant = choice(restaurants)
        if "formatted_address" in restaurant:
            address = restaurant["formatted_address"]
        else:
            address = restaurant["vicinity"]

        loc_message = LocationSendMessage(
            title=f"{restaurant['index']}: {restaurant['name']}",
            address=address,
            latitude=restaurant["geometry"]["location"]["lat"],
            longitude=restaurant["geometry"]["location"]["lng"],
        )
        txt_message = TextSendMessage(f'Google評價: {restaurant["rating"]}')

        return [loc_message, txt_message]

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

    def load_jpgs(self, path="nccueater"):
        jpg_fnames = [str(fname) for fname in Path(path).glob("*.jpg")]
        base_url = "https://nccu-gourmet-linebot.df.r.appspot.com/"
        jpg_urls = [base_url + fname for fname in jpg_fnames]
        return jpg_urls

    def list_restaurants(self, place_type="food", idx=-1):
        if place_type == "food":
            restaurants = self.foods
        elif place_type == "drink":
            restaurants = self.drinks
        elif place_type == "open_now":
            for place in self.all_details:
                pass

        text = ""
        # show specific page
        if idx > 0:
            total_page = math.ceil(len(restaurants) / 10)
            text += f"第{idx}頁/共{total_page}頁\n"
            for restaurant in restaurants[(idx - 1) * 10 : idx * 10]:
                text += f"{restaurant['index']}: {restaurant['name']}\n"
        # show all
        else:
            for restaurant in restaurants:
                text += f"{restaurant['index']}: {restaurant['name']}\n"
        txt_message = TextSendMessage(text=text[:-1])
        return txt_message

    def get_img(self):
        img_path = choice(self.jpg_urls)
        img_message = ImageSendMessage(
            original_content_url=img_path, preview_image_url=img_path
        )
        return img_message

    def about(self):
        text = [
            "開發者: 黃品硯\n",
            "版本: v1.0\n",
            "信箱: pyhuang97@gmail.com\n",
            "更新時間: 2020/11/15",
        ]
        txt_message = TextSendMessage(text="".join(text))
        return txt_message


# %%
if __name__ == "__main__":
    bot = Bot()
    out = bot.handle_message("吃")
    print(out)

# %%
