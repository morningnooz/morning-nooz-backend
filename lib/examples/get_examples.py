from types import SimpleNamespace
from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
import json

cred = credentials.Certificate("./morning-nooz-firebase-adminsdk-23o8s-47a5cd78d0.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://morning-nooz.firebaseio.com'
})
db = firestore.client()
ref = db.collection('examples')
ref.get()

def examples_list():
    docs = ref.get()
    res = []
    for entry in docs:
        try:
            doc = entry.to_dict()
            summ = doc['summary']
            summ_obj = json.loads(summ, object_hook=lambda d: SimpleNamespace(**d))
            new_entry = {
                'topic': doc['topic'],
                'entry': summ_obj
            }
            res.append(new_entry)
        except:
            continue

    return res