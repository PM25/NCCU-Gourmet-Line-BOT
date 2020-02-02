#%% Load API Key
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")

#%% Import Google Maps API Library
import googlemaps

gmaps = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)

#%% Get Restaurant near National Chengchi University (NCCU)
location = (24.9873604, 121.574662)
radius = 150
place_type = "restaurant"
language = "zh-TW"

places_results = gmaps.places(
    query=["restaurant"],
    location=location,
    radius=radius,
    language=language,
    type=place_type,
)

# %% Load Page 2 and Page 3
from time import sleep

results = []
while True:
    for result in places_results.get("results"):
        results.append(result)

    if "next_page_token" in places_results:
        sleep(2)
        page_token = places_results["next_page_token"]
        places_results = gmaps.places_nearby(page_token=page_token)
    else:
        break

# %% Save Results
import pickle

with open("server/restaurants.pickle", "wb") as ofile:
    pickle.dump(results, ofile)


# %%
