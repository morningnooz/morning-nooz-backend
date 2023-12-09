import azure.functions as func
import datetime
import json
import logging
from dotenv import load_dotenv
from app import app as run

app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 28 * * * *",
    arg_name="myTimer",
    run_on_startup=True,
    use_monitor=False,
)
def timer_function(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Executing the Azure Function!")
    # Code goes here:
    load_dotenv()
    run(False)

    logging.info("Python timer trigger function executed.")
