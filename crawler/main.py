#%%
from mylib import *

import pickle

# Database
db = Database()

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
bar_types = ["bar"]
store_types = ["convenience_store", "grocery_or_supermarket", "supermarket"]
food_types = restaurant_types + store_types + ["bakery"]

restaurant_keywords = ["restaurant", "餐廳"]
rice_keywords = ["飯", "rice", "炒飯", "自助餐", "燉飯", "risotto", "飯館", "合菜"]
noodle_keywords = ["麵", "noodle", "炒麵", "湯麵", "義大利麵", "pasta", "義式料理"]
burger_keywords = ["漢堡", "burger", "美式餐廳"]
bar_keywords = ["酒吧", "bar"]
bakery_keywords = ["麵包店", "bakery", "烘培坊"]
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
drink_keywords = ["drink", "飲料", "手搖飲", "飲料店"]
coffee_keywords = ["咖啡店", "cafe"]

# %%
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
]
food_places = nccu.search_types_keywords(food_keywords, restaurant_types)
processed_places = Places_Id(food_places)
processed_places.append_attribute({"mykeywords": "food"})
food_places = processed_places.get_important_info(keys)
db.store(food_places)

drink_places = nccu.search_types_keywords(drink_keywords, drink_types)
processed_places = Places_Id(drink_places)
processed_places.append_attribute({"mykeywords": "drink"})
drink_places = processed_places.get_important_info(keys)
db.store(drink_places)

print(f"*Search foods & drinks completed.")

#%%
utils.places_summary(food_places)
utils.places_summary(drink_places)

#%%



#%%
with open("../data/foods.pickle", "wb") as infile:
    pickle.dump(food_places, infile)

with open("../data/drinks.pickle", "wb") as infile:
    pickle.dump(drink_places, infile)

# %%
keyword_id_tab = {}
for place in food_places + drink_places:
    for keyword in place["keywords"]:
        keyword_id_tab[keyword] = keyword_id_tab.get(keyword, []) + [place["place_id"]]

with open("../data/keyword_id.pickle", "wb") as infile:
    pickle.dump(keyword_id_tab, infile)

# %%
all_places = food_places + drink_places
all_places = nccu.add_index(all_places)

with open("../data/all.pickle", "wb") as infile:
    pickle.dump(all_places, infile)

# %%
id_index_tab = {}
for place in all_places:
    id_index_tab[place["place_id"]] = place["index"]

with open("../data/id_index.pickle", "wb") as infile:
    pickle.dump(id_index_tab, infile)

# %%
with open("../data/all.pickle", "rb") as infile:
    all_places = pickle.load(infile)

places_detail = Places_Id(all_places).get_details()

with open("../data/all_details.pickle", "wb") as ofile:
    pickle.dump(places_detail, ofile)

# %%
