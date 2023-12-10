import azure.functions as func
import logging
import os
import json
from lib.dispatch import dispatch as run_dispatch
from lib.processing import process as run_processing
from lib.send import send_sendgrid_email

from dotenv import load_dotenv

load_dotenv()
storage_connection = os.getenv("STORAGE_CONNECTION")
bp = func.Blueprint()


@bp.timer_trigger(
    schedule="0 30 * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False
)
def dispatch(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Executing the Dispatch Function!")

    prod = False
    if os.getenv("ENV") == "production":
        prod = True

    run_dispatch(prod)

    logging.info("Python timer trigger function executed.")

    logging.info("Python timer trigger function executed.")


@bp.queue_trigger(
    arg_name="azqueue", queue_name="process-queue", connection=storage_connection
)
def process(azqueue: func.QueueMessage):
    message = json.loads(azqueue.get_body().decode("utf-8"))
    logging.info(f"Python Queue trigger processed a message: {message}")

    run_processing(message)


@bp.queue_trigger(
    arg_name="azqueue", queue_name="send-queue", connection=storage_connection
)
def send(azqueue: func.QueueMessage):
    message = json.loads(azqueue.get_body().decode("utf-8"))
    logging.info(f"Python Queue trigger processed a message: {message}")

    send_sendgrid_email(
        email_receiver=message["email"],
        name=message["name"],
        topic=message["topics"],
        summaries=message["summaries"],
    )
