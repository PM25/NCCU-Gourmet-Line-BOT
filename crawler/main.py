#%%
from mylib import *

import pickle


locations = [
    (24.987606, 121.576065),
    (24.987847, 121.574858),
    (24.987362, 121.577173),
    (24.989267, 121.573721),
]

nccu = NCCU_Places(locations)

# %%
restaurant_types = ["restaurant", "meal_delivery", "meal_takeaway"]
drink_types = ["cafe"]
bar_types = ["bar"]
store_types = ["convenience_store", "grocery_or_supermarket", "supermarket"]
food_types = restaurant_types + store_types + ["bakery"]

restaurant_keywords = ["restaurant", "餐廳"]
rice_keywords = ["飯", "rice", "炒飯", "自助餐", "燉飯", "risotto", "飯館", "合菜"]
noodle_keywords = ["麵", "noodle", "炒麵", "湯麵"]
burger_keywords = ["漢堡", "burger"]
bar_keywords = ["酒吧", "bar"]
bakery_keywords = ["麵包店", "bakery"]
store_keywords = [
    "便利商店",
    "超商",
    "賣場",
    "convenience store",
    "grocery",
    "supermarket",
    "store",
]
food_keywords = restaurant_keywords + rice_keywords + noodle_keywords + burger_keywords
drink_keywords = ["drink", "飲料"]
coffee_keywords = ["咖啡店", "cafe"]

# %%
food_places = nccu.search_types_keywords(food_keywords, restaurant_types)
drink_places = nccu.search_types_keywords(drink_keywords, drink_types)

with open("../foods.pickle", "wb") as infile:
    pickle.dump(food_places, infile)

with open("../drinks.pickle", "wb") as infile:
    pickle.dump(drink_places, infile)

# %%
