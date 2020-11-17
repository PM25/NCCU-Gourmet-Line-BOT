#%%
from mylib import *

from datetime import date

# NCCU coordinate
locations = [
    (24.987606, 121.576065),
    (24.987847, 121.574858),
    (24.987362, 121.577173),
    (24.989267, 121.573721),
    (24.987075, 121.578359),
]

nccu = NCCU_Places(locations)

# %%
restaurant_types = ["restaurant", "meal_delivery", "meal_takeaway"]
drink_types = ["cafe"]

restaurant_keywords = ["restaurant", "餐廳"]
rice_keywords = ["飯", "rice", "炒飯", "自助餐", "燉飯", "risotto", "飯館", "合菜"]
noodle_keywords = ["麵", "noodle", "炒麵", "湯麵", "義大利麵", "pasta", "義式料理"]
burger_keywords = ["漢堡", "burger", "美式餐廳"]
food_keywords = restaurant_keywords + rice_keywords + noodle_keywords + burger_keywords

drink_keywords = ["drink", "飲料", "手搖飲", "飲料店"]

# %%
# column's name to keep
keys = [
    "index",
    "name",
    "vicinity",
    "geometry",
    "keywords",
    "types",
    "place_id",
    "opening_hours",
    "rating",
    "formatted_phone_number",
    "mykeywords",
    "last_update"
]

# database
db = Database()

# search restaurants
food_places = nccu.search_types_keywords(food_keywords, restaurant_types)
processed_food_places = Places_Id(food_places)
processed_food_places.append_attribute({"mykeywords": "food", "last_update": str(date.today())})
food_places = processed_food_places.get_important_info(keys)
db.store(food_places)

# search drink store
drink_places = nccu.search_types_keywords(drink_keywords, drink_types)
processed_drink_places = Places_Id(drink_places)
processed_drink_places.append_attribute({"mykeywords": "drink", "last_update": str(date.today())})
drink_places = processed_drink_places.get_important_info(keys)
db.store(drink_places)

print(f"*Search foods & drinks completed.")

#%%
utils.places_summary(food_places)
utils.places_summary(drink_places)

# %%
