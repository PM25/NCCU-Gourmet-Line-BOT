from time import sleep
from mylib.google_maps_api import Google_Maps_API


# search by keywords or types near NCCU locations
class NCCU_Places(Google_Maps_API):
    def __init__(self, locations=[(24.9862, 121.5771)], language="zh-TW", rank_by="distance"):
        super().__init__()
        self.locations = locations
        self.language = language
        self.rank_by = rank_by
        # only get places inside restrict area.
        self.restrict_area = {
            "lng": [121.572230, 121.579120],
            "lat": [24.986530, 24.989550],
        }

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

    # Get all the places around locations with keywords and types
    def search_types_keywords(self, keywords=["restaurant", "餐廳"], types=["restaurant"]):
        results = []
        results += self.search_keywords(types, method="type")
        results += self.search_keywords(keywords, method="keyword")
        results = self.remove_dup(results)
        results = self.add_index(results)
        return results

    # Get all the places around locations with keywords or types
    def search_keywords(self, keywords=["restaurant"], method="keyword"):
        results = []
        for keyword in keywords:
            results += self.search_keyword(keyword, method)
            results = self.add_keyword(results, keyword)
        results = self.remove_dup(results)
        return results

    # Get all the places around loactions with only one keyword or type
    def search_keyword(self, keyword, method):
        results = []
        for location in self.locations:
            for place_result in self.get_places(location, keyword, method):
                result_loc = place_result["geometry"]["location"]
                if self.check_loc(result_loc["lat"], result_loc["lng"]):
                    results.append(place_result)
        return results

    # Get all the places around with one location and one keyword or type
    def get_places(self, location, keyword, method):
        print(f"*Searching {keyword} near location {location}.")
        if method == "keyword":
            places_results = self.gmaps.places_nearby(
                location=location,
                language=self.language,
                keyword=keyword,
                rank_by=self.rank_by,
            )
        elif method == "type":
            places_results = self.gmaps.places_nearby(
                location=location,
                language=self.language,
                type=keyword,
                rank_by=self.rank_by,
            )
        else:
            raise ValueError("unsupported method value.")

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

    # Given a list of results of Places API and remove the duplicates
    def remove_dup(self, places):
        results = {}
        for place in places:
            place_id = place["place_id"]
            if place_id in results:
                place["keywords"] += results[place_id]["keywords"]
            results[place_id] = place
        results = list(results.values())
        for result in results:
            result["keywords"] = list(set(result["keywords"]))
        return results

    # Given a list of results of Places API and add keyword attributes to them
    def add_keyword(self, places, keyword):
        for place in places:
            place["keywords"] = place.get("keywords", []) + [keyword]
        return places

    # Given a list of results of Places API and add index attributes to them
    def add_index(self, places):
        for idx, place in enumerate(places, 1):
            place["index"] = idx
        return places
