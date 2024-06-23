import logging
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from string import Template
from datetime import datetime


def send_sendgrid_email(email_receiver, name, topic, summaries):
    body_msg = Template(
        """<em>Hello, $name!</em><br><br>Unfortunately there was an error while processing your news this morning😢<br><br>
    """
    ).substitute(name=name)
    if len(summaries) > 0:
        body_msg = summaries

    email_sender = os.getenv("SENDER_EMAIL")
    logging.info(email_sender)

    now = datetime.now()
    formatted_date = now.strftime("%B %d, %Y")

    message = Mail(
        from_email=email_sender,
        to_emails=[email_receiver, email_sender],
        subject=(f"Your Daily Digest - {formatted_date}"),
        html_content=body_msg,
    )
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        logging.info(response.status_code)
        logging.info(response.body)
        logging.info(response.headers)

        logging.info(f"email sent to {name}")
    except Exception as e:
        logging.error(e)
