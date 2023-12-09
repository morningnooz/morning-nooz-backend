from types import SimpleNamespace
import json
from string import Template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from firebase_admin import firestore
from firebase_admin import credentials
import os

import sys
import firebase_admin
import logging

from app.text_processing import build_email

email_sender = os.getenv("SENDER_EMAIL")
email_password = os.getenv("SENDER_PASSWORD")


def app(prod: bool):
    logging.info("in prod", prod)
    cred = credentials.Certificate(
        "./app/morning-nooz-firebase-adminsdk-23o8s-47a5cd78d0.json"
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
        email = doc_data["email"]
        topics = doc_data["topics"]
        name = doc_data["name"]

        summary_list = ""
        counter = 0
        while len(summary_list) == 0 and counter < 10:
            try:
                logging.info("summary attempt ", counter)
                summary_list = build_email(topics)
                break
            except:
                logging.info("summary attempt failed")
                counter += 1
        send_sendgrid_email(email, name, topics, summary_list)


def send_sendgrid_email(email_receiver, name, topic, summaries):
    body_msg = Template(
        """<em>Hello, $name!</em><br><br>Unfortunately there was an error while processing your news this morning😢<br><br>
    """
    ).substitute(name=name)
    if len(summaries) > 0:
        body = Template(
            "<em>Hello, $name!</em><br><br>Hope you've been well! Update your topics at <a href='morningnooz.com'>morningnooz.com</a>.<br>Here is your weekly digest:<br><br> $summaries"
        )
        body_msg = body.substitute(name=name, topic=topic, summaries=summaries)

    email_sender = os.getenv("SENDER_EMAIL")
    logging.info(email_sender)

    message = Mail(
        from_email=email_sender,
        to_emails=email_receiver,
        subject=("Your Weekly Nooz"),
        html_content=body_msg,
    )
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        logging.info(response.status_code)
        logging.info(response.body)
        logging.info(response.headers)

        logging.info("email sent to " + name)
        logging.info("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
    except Exception as e:
        logging.info(e)


def get_firebase_data(db, prod: bool):
    # Get a database reference
    ref = db.collection("users") if prod else db.collection("test-users")

    # Retrieve the data
    data = ref.get()

    return data


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "prod":
        app(prod=True)
    else:
        app(prod=False)
