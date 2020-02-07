#%%
from mylib import *

locations = [
    (24.989267, 121.573721),
    (24.987847, 121.574858),
    (24.987606, 121.576065),
    (24.987362, 121.577173),
]
place_types = [
    "cafe",
    "bakery",
    "bar",
    "convenience_store",
    "grocery_or_supermarket",
    "meal_delivery",
    "meal_takeaway",
    "restaurant",
    "supermarket",
]
keywords = ["drink", "飲料", "restaurant", "餐廳"]


nccu = NCCU_Places_By_Keyword(locations)
places = nccu.get_all_places(keywords)

nccu = NCCU_Places_By_Types(locations)
places = nccu.get_all_places(place_types)
