from processing.process import run_process
from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
import json
import logging

cred = credentials.Certificate("./morning-nooz-firebase-adminsdk-23o8s-47a5cd78d0.json")

firebase_admin.initialize_app(
    cred, {"databaseURL": "https://morning-nooz.firebaseio.com"}
)
db = firestore.client()

ref = db.collection("examples")
# Retrieve the data
# data = ref.get()


def topic_exists(topic, collection):
    query = collection.where("topic", "==", topic)
    res = query.get()
    logging.info("RES", res)
    return len(res) > 0


file_path = "./examples/topics.txt"
with open(file_path, "r") as file:
    for top in file:
        topic = top.strip()
        if topic_exists(topic, ref):
            logging.info(topic + " - SKIP")
        else:
            logging.info(topic + " - starting")
            res = run_process(topic)
            json_res = str(res)
            new_entry = {"topic": topic, "summary": res}
            ref.add(new_entry)
            logging.info("---new entry---")
            logging.info(new_entry)
            logging.info("---------------")
            logging.info(topic + " - finished")
