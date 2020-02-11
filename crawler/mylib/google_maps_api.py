import os
import googlemaps
from dotenv import load_dotenv, find_dotenv


class Google_Maps_API:
    def __init__(self):
        self.gmaps = self.get_google_maps_client()

    # Load API Key & Import Google Maps API Library
    def get_google_maps_client(self):
        load_dotenv(find_dotenv())
        GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
        gmaps = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
        return gmaps
