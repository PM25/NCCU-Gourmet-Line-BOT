#%%
from mylib import *

import pickle


locations = [
    (24.987606, 121.576065),
    (24.987847, 121.574858),
    (24.987362, 121.577173),
    (24.989267, 121.573721),
]

search_by_types = NCCU_Places_By_Types(locations)
search_by_keywords = NCCU_Places_By_Keyword(locations)


def get_all_places(keywords, place_types=[]):
    places = []
    places += search_by_types.get_all_places(place_types)
    places += search_by_keywords.get_all_places(keywords)
    return places


def save(data, fname):
    with open(fname, "wb") as ofile:
        pickle.dump(data, ofile)


#%% Get all restaurants around NCCU
place_types = ["restaurant", "meal_delivery", "meal_takeaway"]
keywords = ["restaurant", "餐廳"]
restaurants = get_all_places(keywords, place_types)

#%% Get all drink shop around NCCU
keywords = ["drink", "飲料"]
drink_shops = get_all_places(keywords)

#%% Get all store around NCCU
place_types = ["convenience_store", "grocery_or_supermarket", "supermarket"]
keywords = ["便利商店", "超商", "賣場", "convenience store", "grocery", "supermarket", "store"]
stores = get_all_places(keywords, place_types)

#%% all bakery around NCCU
place_types = ["bakery"]
keywords = ["麵包店", "bakery"]
bakerys = get_all_places(keywords, place_types)

#%% Get all cafe around NCCU
place_types = ["cafe"]
keywords = ["咖啡店", "cafe"]
cafes = get_all_places(keywords, place_types)

#%% Get all bar around NCCU
place_types = ["bar"]
keywords = ["酒吧", "bar"]
bars = get_all_places(keywords, place_types)

#%% Get all restaurants around NCCU that provides rice
keywords = ["飯", "rice", "炒飯", "自助餐", "燉飯", "risotto", "飯館", "合菜"]
rice = get_all_places(keywords)
save(rice, "server/rice.pickle")

# %%
#%% Get all restaurants around NCCU that provides rice
keywords = ["麵", "noodle", "炒麵", "湯麵"]
noodle = get_all_places(keywords)
save(noodle, "../server/noodle.pickle")

# %%
place_types = ["cafe"]
keywords = ["咖啡店", "cafe"]
cafes = search_by_keywords.remove_dup(get_all_places(keywords, place_types))

# %%
