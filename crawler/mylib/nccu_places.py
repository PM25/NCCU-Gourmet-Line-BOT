import os
import googlemaps
from dotenv import load_dotenv, find_dotenv


class NCCU_Places:
    def __init__(self, locations, language="zh-TW", rank_by="distance"):
        self.locations = locations
        self.language = language
        self.rank_by = rank_by
        self.restrict_area = {
            "lng": [121.572230, 121.579120],
            "lat": [24.986530, 24.989550],
        }
        self.gmaps = self.get_google_maps_client()

    # Check if the given loaction is inside the restrict area
    def check_loc(self, lat, lng):
        lng_range = self.restrict_area["lng"]
        lat_range = self.restrict_area["lat"]
        if lng < lng_range[0] or lng > lng_range[1]:
            return False
        elif lat < lat_range[0] or lat > lat_range[1]:
            return False
        else:
            return True

    # Load API Key & Import Google Maps API Library
    def get_google_maps_client(self):
        load_dotenv(find_dotenv())
        GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
        gmaps = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
        return gmaps
