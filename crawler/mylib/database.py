#%%
from google.cloud import firestore


class Database:
    def __init__(self):
        self.db = firestore.Client()
        self.db_places = self.db.collection("places2")

    def store(self, places):
        for place in places:
            db_ref = self.db_places.document(place["place_id"])
            db_ref.set(place, merge=True)
