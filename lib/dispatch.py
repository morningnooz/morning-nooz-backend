import os
import logging
import firebase_admin
import datetime
from firebase_admin import firestore
from firebase_admin import credentials

from lib.utils import send_message_to_queue


email_sender = os.getenv("SENDER_EMAIL")
email_password = os.getenv("SENDER_PASSWORD")


def dispatch(prod: bool):
    logging.info(f"in prod {prod}")
    cred = credentials.Certificate(
        "./lib/morning-nooz-firebase-adminsdk-23o8s-47a5cd78d0.json"
    )
    if not firebase_admin._apps:
        firebase_admin.initialize_app(
            cred, {"databaseURL": "https://morning-nooz.firebaseio.com"}
        )
    db = firestore.client()

    data = get_firebase_data(db, prod)

    dispatch_list = []
    for doc in data:
        doc_data = doc.to_dict()
        # get current day from time
        current_day = datetime.datetime.now().strftime("%A").lower()
        if doc_data["day"] == current_day:
            dispatch_list.append(doc_data)

    return dispatch_list


def get_firebase_data(db, prod: bool):
    # Get a database reference
    ref = db.collection("profiles") if prod else db.collection("test-users")

    # Retrieve the data
    data = ref.get()

    return data
