import azure.functions as func
import logging
import os
import base64
import json
from lib.dispatch import dispatch as run_dispatch
from lib.process import process as run_processing
from lib.send import send_sendgrid_email
from lib.utils import send_message_to_queue

from dotenv import load_dotenv

load_dotenv()
bp = func.Blueprint()


@bp.timer_trigger(
    schedule="0 3 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False
)
def dispatch(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Executing the Dispatch Function!")

    prod = False
    if os.getenv("ENV") == "production":
        prod = True

    to_dispatch = run_dispatch(prod)

    for doc in to_dispatch:
        doc_data = doc.to_dict()
        send_message_to_queue(
            doc_data, "process-queue", os.getenv("STORAGE_CONNECTION")
        )

    logging.info("Python timer trigger function executed.")


@bp.queue_trigger(
    arg_name="azqueue", queue_name="process-queue", connection="AzureWebJobsStorage"
)
def process(azqueue: func.QueueMessage):
    message = json.loads(azqueue.get_body().decode("utf-8"))
    logging.info(f"[PROCESS] Process Queue trigger. Processing a message: {message}")

    to_send = run_processing(message)

    try:
        send_message_to_queue(
            to_send,
            "send-queue",
            os.getenv("STORAGE_CONNECTION"),
        )
    except:
        logging.error(f"Error queueing process queue: {message}")

    logging.info(f"[PROCESS] message processed: {message}")


@bp.queue_trigger(
    arg_name="azqueue", queue_name="send-queue", connection="AzureWebJobsStorage"
)
def send(azqueue: func.QueueMessage):
    message = json.loads(azqueue.get_body().decode("utf-8"))
    logging.info(f"[SEND] Send Queue trigger. Processing a message: {message}")

    send_sendgrid_email(
        email_receiver=message["email"],
        name=message["name"],
        topic=message["topics"],
        summaries=message["summaries"],
    )
    logging.info(f"[SEND] message sent: {message}")
