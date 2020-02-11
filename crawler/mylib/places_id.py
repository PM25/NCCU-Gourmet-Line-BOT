from time import sleep
from mylib.google_maps_api import Google_Maps_API


class Places_Id(Google_Maps_API):
    def __init__(self, ids, language="zh-TW"):
        super().__init__()
        self.ids = ids
        self.language = language

    def get_details(self):
        results = []
        for place_id in self.ids:
            place_detail = self.gmaps.place(place_id=place_id, language=self.language)
            results.append(place_detail["result"])
        return results
