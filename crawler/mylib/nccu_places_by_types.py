from mylib.nccu_places import NCCU_Places

from time import sleep


class NCCU_Places_By_Types(NCCU_Places):
    def __init__(self, locations, place_types):
        super().__init__(locations)
        self.place_types = place_types

    def get_places(self, location, place_type):
        print(f"*Searching {place_type} near location {location}.")
        places_results = self.gmaps.places_nearby(
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
            places_results = self.gmaps.places_nearby(
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
