#%%
from mylib import NCCU_Places_By_Keyword, NCCU_Places_By_Types

# %%
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

# %%
keywords = ["drink", "飲料"]
nccu = NCCU_Places_By_Keyword(locations, keywords)
places = nccu.get_all_places()

# %%
all_places = []
for place_type in keywords:
    all_places += places[place_type]
