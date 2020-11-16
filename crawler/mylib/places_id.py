from time import sleep
from mylib.google_maps_api import Google_Maps_API


class Places_Id(Google_Maps_API):
    def __init__(self, places, language="zh-TW"):
        super().__init__()
        self.language = language
        self.places = places
        self.ids = self.get_ids(self.places)
        self.places_all_info = self.get_all_info()

    def get_ids(self, places):
        return [place["place_id"] for place in places]

    def append_attribute(self, attr: dict):
        self.updated_places = []
        for place in self.places_all_info.copy():
            place.update(attr)
            self.updated_places.append(place)
        self.places_all_info = self.updated_places

    def get_important_info(self, keys=["index", "name", "place_id"]):
        places_important_info = []
        for place in self.places_all_info:
            filted_place = {key: place.get(key, "") for key in keys}
            places_important_info.append(filted_place)
        return places_important_info

    def get_all_info(self):
        places_all_info = []
        places_detail = self.get_details()
        for place in self.places.copy():
            place_id = place["place_id"]
            place.update(places_detail[place_id])
            places_all_info.append(place)
        return places_all_info

    def get_details(self):
        results, failed = {}, []
        for place_id in self.ids:
            try:
                print(f"*fetching id({place_id})'s detail.")
                place_detail = self.gmaps.place(
                    place_id=place_id, language=self.language
                )
                results[place_id] = place_detail["result"]
            except:
                failed.append(place_id)

        if len(failed) > 0:
            print(f"Can't find these ids' detail: {failed}.")
        return results
