import os

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from dotenv import load_dotenv


load_dotenv()
account_sid = os.getenv("MS_TWILIO_ACCOUNT_SID")
api_sid = os.getenv("MS_TWILIO_API_KEY_SID")
api_secret = os.getenv("MS_TWILIO_API_KEY_SECRET")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
user_number = os.getenv("USER_PHONE_NUMBER")
client = Client(api_sid , api_secret , account_sid)


def send_message(message):
    try:
        message = client.messages.create(
            to=f"whatsapp:{user_number}",
            from_=f"whatsapp:{twilio_number}",
            body=message)
        print(message.sid)
    except TwilioRestException as e:
        print(f"Error: {e}")


#send_message("Test test does this work?")
my_message_sid = "SM838fb1d804a6bec3d4548f254b6d946e"
my_message = client.messages(my_message_sid).fetch()

print(f"Message Status: {my_message.status}")
