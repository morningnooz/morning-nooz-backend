import os
import logging
import firebase_admin
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

    # iterate through data, and send email for each entry
    for doc in data:
        doc_data = doc.to_dict()
        send_message_to_queue(
            doc_data, "process-queue", os.getenv("STORAGE_CONNECTION")
        )


def get_firebase_data(db, prod: bool):
    # Get a database reference
    ref = db.collection("users") if prod else db.collection("test-users")

    # Retrieve the data
    data = ref.get()

    return data
