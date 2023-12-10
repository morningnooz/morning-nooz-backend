import azure.functions as func
import datetime
import json
import logging
import os
from dotenv import load_dotenv
from lib import app as run

app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 42 * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def timer_function(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Executing the Azure Function!")
    # Code goes here:
    load_dotenv()

    prod = False
    if os.getenv("ENV") == "production":
        prod = True

    run(prod)

    logging.info("Python timer trigger function executed.")
