import yagmail
from twilio.rest import Client
from config import *

def send_email(to, subject, content):
    yag = yagmail.SMTP(EMAIL_SENDER, EMAIL_PASSWORD)
    yag.send(to, subject, content)

def send_sms(to, message):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=to
    )
