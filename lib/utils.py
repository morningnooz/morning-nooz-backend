import logging
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage


def send_message_to_queue(message, queue_name, connection_string):
    # Create a QueueClient
    queue_client = QueueClient.from_connection_string(connection_string, queue_name)

    # Send a message
    response = queue_client.send_message(message)
    logging.info(f"Message added to {queue_name}: {response}")
