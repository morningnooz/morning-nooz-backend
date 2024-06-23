import json
import base64
import logging
from azure.storage.queue import QueueClient
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

def send_message_to_queue(message, queue_name, connection_string):
    # Create a QueueClient
    queue_client = QueueClient.from_connection_string(connection_string, queue_name)

    try:
        # Check if the message is JSON serializable
        json_data = json.dumps(message)
        # If JSON serialization is successful, convert to bytes
        message = json_data.encode("utf-8")
    except TypeError:
        # If it's not JSON serializable, check if it's already a byte or string
        if isinstance(message, str):
            message = message.encode("utf-8")
        elif not isinstance(message, bytes):
            raise ValueError("Message must be JSON serializable, a string, or bytes")

    # Base64 encode the message
    base64_encoded_message = base64.b64encode(message).decode("utf-8")

    # Send the message
    response = queue_client.send_message(base64_encoded_message)
    logging.info(f"Message added to {queue_name}: {response.id}")

def send_message_to_db(message, user_id):
    try:
        # Attempt to initialize the app
        cred = credentials.Certificate(
            "./lib/morning-nooz-firebase-adminsdk-23o8s-47a5cd78d0.json"
        )
        firebase_admin.initialize_app(
            cred, {"databaseURL": "https://morning-nooz.firebaseio.com"}
        )
        logging.info('Firebase app initialized.')
    except ValueError as e:
        # Firebase app is already initialized
        logging.info('Firebase app already initialized.')
    except Exception as e:
        # Other exceptions
        logging.error(f"An error occurred while initializing Firebase app: {e}")
        return

    logging.info('Connected to Firebase.')
    
    try:
        db = firestore.client()
        # drop the entry in
        ref = db.collection("nysignal-users")
        logging.info('connected to collection')
        logging.info(f"user_id: {user_id}")

        # Retrieve the data
        doc = ref.document(user_id)
        logging.info(f"doc connected: {doc}")
        doc.set(message)
        logging.info(f"Document created. Label: {user_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
