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
chat_service_sid = os.getenv("CHAT_SERVICE_SID")

client = Client(api_sid, api_secret, account_sid)
print("Client initialized:", client)


def send_text_message(text):
    """sends a text message (provided in the arguments) to the user_number via whatsapp"""
    try:
        message = client.messages.create(
            to=f"whatsapp:{user_number}",
            from_=f"whatsapp:{twilio_number}",
            body=text)
        print(message.status)
    except TwilioRestException as e:
        print(f"An error has occurred: {e}")
    except Exception as e:
        print(f"An unexpected error has occurred: {e}")


def send_msg_with_media(from_whatsapp, to_whatsapp, body, media_url):
    """
    send a message that includes media, media provided with url (e.g. jpg)
    """
    try:
        message = client.messages.create(
            from_=f"whatsapp:{from_whatsapp}",  # Twilio sandbox WhatsApp number
            body=body,
            media_url=[media_url],
            to=f"whatsapp:{to_whatsapp}"  # Recipient's WhatsApp number
        )
        print(message.sid)
    except TwilioRestException as e:
        print(f"An error has occurred: {e}")
    except Exception as e:
        print(f"An unexpected error has occurred: {e}")


def update_conversation_friendly_name(a_conversation_sid, friendly_name: str):
    """
    the conversations were given real phone numbers as friendly name,
    but if we don't want that, we can change it with this
    no error handling yet, please only give valid conversation sid and str
    """
    service_conversation = (
        client.conversations.v1.services(chat_service_sid)
        .conversations(a_conversation_sid)
        .update(friendly_name=friendly_name)
    )


def list_conversations(a_chat_service_sid):
    """
    lists conversations from Twilio in a specific chat service
    """
    conversations = client.conversations.v1.services(a_chat_service_sid).conversations.list()

    for conversation in conversations:
        print(f"Conversation SID: {conversation.sid}, Conversation status: {conversation.state}")


def get_conversation_sids():
    conversations = client.conversations.v1.services(chat_service_sid).conversations.list()
    conversation_sids_list = []
    for conversation in conversations:
        if conversation.sid not in conversation_sids_list:
            conversation_sids_list.append(conversation.sid)

    return conversation_sids_list


def retrieve_latest_message():
    """gets last two messages sent by the user into the whatsapp chat and returns them in a list of strings"""
    messages = client.messages.list(
        limit=1
    )

    if messages:
        latest_message = messages[0]
        if latest_message.to == f"whatsapp:{twilio_number}" and latest_message.from_ == f"whatsapp:{user_number}":
            return latest_message.body
