import json
import base64
import logging
from azure.storage.queue import QueueClient


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
