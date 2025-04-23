"""
rich content part not working yet
"""


import os

import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv


load_dotenv()

# These values come from your Twilio Console
account_sid = os.getenv("MS_TWILIO_ACCOUNT_SID")
api_key_sid = os.getenv("MS_TWILIO_API_KEY_SID")
api_key_secret = os.getenv("MS_TWILIO_API_KEY_SECRET")
twilio_whatsapp = os.getenv("TWILIO_PHONE_NUMBER")
user_whatsapp = os.getenv("USER_PHONE_NUMBER")

# API endpoint for sending messages
url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"


def send_message(message, from_whatsapp, to_whatsapp):
    # Payload for sending a WhatsApp message
    payload = {
        "To": f"whatsapp:{to_whatsapp}",
        "From": f"whatsapp:{from_whatsapp}",
        "Body": message
    }

    # Make the request with API Key + Secret
    response = requests.post(
        url,
        data=payload,
        auth=HTTPBasicAuth(api_key_sid, api_key_secret)
    )

    print(response.status_code)
    print(response.json())
send_message("Sending via http service", twilio_whatsapp, user_whatsapp)


def send_interactive_message(from_whatsapp, to_whatsapp):
# Interactive message payload
    payload = {
        "To": f"whatsapp:{to_whatsapp}",
        "From": f"whatsapp:{from_whatsapp}",
        "MessagingServiceSid": "your_messaging_service_sid_if_needed",  # Optional
        "ContentSid": "",  # Not used for this raw API
        "PersistentAction": "",
        "Body": "",  # Leave empty, we use 'interactive'
        "Content": {
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": "Choose your meme type 🎭"
                },
                "action": {
                    "button": "Pick a meme",
                    "sections": [
                        {
                            "title": "Meme Options",
                            "rows": [
                                {
                                    "id": "meme_day",
                                    "title": "Meme of the Day"
                                },
                                {
                                    "id": "meme_week",
                                    "title": "Meme of the Week"
                                },
                                {
                                    "id": "meme_month",
                                    "title": "Meme of the Month"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }

    # Send the request
    response = requests.post(
        url,
        auth=HTTPBasicAuth(api_key_sid, api_key_secret),
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    # Print response
    print(response.status_code)
    print(response.text)

send_interactive_message(twilio_whatsapp, user_whatsapp)