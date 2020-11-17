#%%
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# initialize firebase
if not firebase_admin._apps:
    try:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {"projectId": "nccu-gourmet-linebot"})
    except:
        cred = credentials.Certificate("firebase-credential.json")
        firebase_admin.initialize_app(cred)


# interface with my database
class Database:
    def __init__(self):
        self.db = firestore.client()
        self.db_places = self.db.collection("places")

    def store(self, places):
        for place in places:
            db_ref = self.db_places.document(place["place_id"])
            db_ref.set(place, merge=True)

    def get_collection(self, col):
        return self.db.collection(col)
