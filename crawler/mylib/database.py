#%%
from pymongo import MongoClient


class Database:
    def __init__(self):
        client = MongoClient("localhost", 27017)
        self.db = client.database
        self.db_places = self.db.places

    def store(self, places):
        for place in places:
            self.db_places.replace_one(
                {"place_id": place["place_id"]}, place, upsert=True
            )


# %%
