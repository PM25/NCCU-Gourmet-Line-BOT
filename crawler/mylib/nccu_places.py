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

    # Given a list of results of Places API and remove the duplicates
    def remove_dup(self, places):
        existed_id, results = [], []
        for place in places:
            if place["id"] not in existed_id:
                existed_id.append(place["id"])
                results.append(place)
        return results

    # Get all the places around locations with keywords or types
    def get_all_places(self, keywords):
        results = []
        for keyword in keywords:
            results += self.get_all_places_by_keyword(keyword)
        results = self.remove_dup(results)
        return results

    # Get all the places around loactions with only one keyword or type
    def get_all_places_by_keyword(self, keyword):
        results = []
        for location in self.locations:
            for place_result in self.get_places(location, keyword):
                result_loc = place_result["geometry"]["location"]
                if self.check_loc(result_loc["lat"], result_loc["lng"]):
                    results.append(place_result)
        return results

    # Abstract Method to get all places around with one location and one keyword or type
    def get_places(self, location, keyword):
        raise NotImplementedError("Must override get_places()")
