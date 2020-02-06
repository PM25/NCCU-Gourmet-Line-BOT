#%% Load API Key & Import Google Maps API Library
import os
import googlemaps
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
gmaps = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)

#%%
from time import sleep


class NCCU_Restaurants:
    def __init__(self, locations, place_types):
        self.locations = locations
        self.place_types = place_types
        self.language = "zh-TW"
        self.rank_by = "distance"
        self.restrict_area = {
            "lng": [121.572230, 121.579120],
            "lat": [24.986530, 24.989550],
        }

    def get_places(self, location, place_type):
        print(f"*Searching {place_type} near location {location}.")
        places_results = gmaps.places_nearby(
            location=location,
            language=self.language,
            type=place_type,
            rank_by=self.rank_by,
        )

        results = places_results["results"]
        # Get Second and Third page result
        while "next_page_token" in places_results:
            sleep(2)
            page_token = places_results["next_page_token"]
            places_results = gmaps.places_nearby(
                page_token=page_token, language=self.language
            )
            results += places_results["results"]

        return results

    def get_all_places_by_type(self, place_type):
        results = []
        for location in self.locations:
            for place_result in self.get_places(location, place_type):
                result_loc = place_result["geometry"]["location"]
                if self.check_loc(result_loc["lat"], result_loc["lng"]):
                    results.append(place_result)
        return results

    def get_all_places(self):
        results = {}
        for place_type in self.place_types:
            results[place_type] = self.get_all_places_by_type(place_type)
        return results

    def check_loc(self, lat, lng):
        lng_range = self.restrict_area["lng"]
        lat_range = self.restrict_area["lat"]
        if lng < lng_range[0] or lng > lng_range[1]:
            return False
        elif lat < lat_range[0] or lat > lat_range[1]:
            return False
        else:
            return True


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

nccu = NCCU_Restaurants(locations, place_types)
places = nccu.get_all_places()

# %%
all_places = []
for place_type in place_types:
    all_places += places[place_type]

# %%
