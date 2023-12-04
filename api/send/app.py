from string import Template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from firebase_admin import firestore
from firebase_admin import credentials

import sys
import firebase_admin

from text_processing import build_email

email_sender = 'morning.nooz@gmail.com'
email_password = 'ykuxcyhyheyamjzb'

def app(prod: bool):
    print('in prod', prod)
    cred = credentials.Certificate("./morning-nooz-firebase-adminsdk-23o8s-47a5cd78d0.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://morning-nooz.firebaseio.com'
    })
    db = firestore.client()

    data = get_firebase_data(db, prod)

    # iterate through data, and send email for each entry
    for doc in data:
        doc_data = doc.to_dict()
        email = doc_data['email']
        topics = doc_data['topics']
        name = doc_data['name']


        summary_list = ''
        counter = 0
        while len(summary_list) == 0 and counter < 10:
            try:
                print('summary attempt ', counter)
                summary_list = build_email(topics)
                break
            except:
                print('summary attempt failed')
                counter += 1
        send_sendgrid_email(email, name, topics, summary_list)

        print('email sent to ' + name)
        print('_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-')

def send_sendgrid_email(email_receiver, name, topic, summaries):
    body_msg = Template("<em>Hello, $name!</em><br><br>Unfortunately there was an error while processing your news this morning😢<br><br>").substitute(name=name)
    if len(summaries) > 0:
        body = Template("<em>Hello, $name!</em><br><br>Hope you've been well! Update your topics at <a href='morningnooz.com'>morningnooz.com</a>.<br>Here is your weekly digest:<br><br> $summaries")
        body_msg = body.substitute(name=name, topic=topic, summaries=summaries)

    message = Mail(
        from_email=email_sender,
        to_emails=[email_receiver, email_sender],
        subject=('Your Weekly Nooz'),
        html_content=body_msg)
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

def get_firebase_data(db, prod: bool):
    # Get a database reference
    ref = db.collection('users') if prod else db.collection('test-users2')
    
    # Retrieve the data
    data = ref.get()

    return data

if __name__== "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'prod':
        app(prod=True)
    else:
        app(prod=False)