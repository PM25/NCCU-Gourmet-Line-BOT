#%%
from mylib import *

locations = [
    (24.989267, 121.573721),
    (24.987847, 121.574858),
    (24.987606, 121.576065),
    (24.987362, 121.577173),
]

search_by_types = NCCU_Places_By_Types(locations)
search_by_keywords = NCCU_Places_By_Keyword(locations)

#%% Get all restaurants around NCCU
place_types = ["restaurant", "meal_delivery", "meal_takeaway"]
keywords = ["restaurant", "餐廳"]

restaurants = []
restaurants += search_by_types.get_all_places(place_types)
restaurants += search_by_keywords.get_all_places(keywords)

#%% Get all drink shop around NCCU
keywords = ["drink", "飲料"]
drink_shops = search_by_keywords.get_all_places(keywords)

#%% Get all store around NCCU
place_types = ["convenience_store", "grocery_or_supermarket", "supermarket"]
keywords = ["便利商店", "超商", "賣場", "convenience store", "grocery", "supermarket", "store"]

stores = []
stores += search_by_types.get_all_places(place_types)
stores += search_by_keywords.get_all_places(keywords)

#%% all bakery around NCCU
place_types = ["bakery"]
keywords = ['麵包店', "bakery"]

bakerys = []
bakerys += search_by_types.get_all_places(place_types)
bakerys += search_by_keywords.get_all_places(keywords)

#%% Get all cafe around NCCU
place_types = ["cafe"]
keywords = ['咖啡店', "cafe"]

cafes = []
cafes += search_by_types.get_all_places(place_types)
cafes += search_by_keywords.get_all_places(keywords)

#%% Get all bar around NCCU
place_types = ["bar"]
keywords = ['酒吧', "bar"]

bars = []
bars += search_by_types.get_all_places(place_types)
bars += search_by_keywords.get_all_places(keywords)