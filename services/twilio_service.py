import os
import time
import datetime
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from dotenv import load_dotenv

# get random meme

# presentation *** andrew and lukas

# connect database *** elinor

# build the loop better, using msg numbers *** xiao

# new user:
# my name is xxxx

# ai generator - url jpg

# dropdown menu / text menu *** raquel
# 1 random meme
# 2 make your own meme
# 3 meme of the day

## when more people are connecting at the same time

load_dotenv()

account_sid = os.getenv("MS_TWILIO_ACCOUNT_SID")
api_sid = os.getenv("MS_TWILIO_API_KEY_SID")
api_secret = os.getenv("MS_TWILIO_API_KEY_SECRET")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
user_number = os.getenv("USER_PHONE_NUMBER")
chat_service_sid = os.getenv("CHAT_SERVICE_SID")
programmer_conversation_sid = os.getenv("CONVERSATION_SID")

client = Client(api_sid, api_secret, account_sid)
print("Client initialized:", client)


def send_text_message(to_whatsapp, text):
    """sends a text message (provided in the arguments) to the user_number via whatsapp"""
    try:
        message = client.messages.create(
            to=f"whatsapp:{to_whatsapp}",
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
# update_conversation_friendly_name(programmer_conversation_sid, "Subscriber +49number")



def get_conversation_sids():
    conversations = client.conversations.v1.services(chat_service_sid).conversations.list()
    conversation_sids_list = []
    for conversation in conversations:
        if conversation.sid not in conversation_sids_list:
            conversation_sids_list.append(conversation.sid)

    return conversation_sids_list

print(get_conversation_sids())


def retrieve_latest_message():
    """gets last two messages sent by the user into the whatsapp chat and returns them in a list of strings"""
    messages = client.messages.list(
        limit=1
    )

    if messages:
        latest_message = messages[0]
        if latest_message.to == f"whatsapp:{twilio_number}" and latest_message.from_ == f"whatsapp:{user_number}":
            return latest_message.body


def detect_new_incoming_msg(a_chat_service_sid: str, user_data: dict):
    """
    loop through conversations to find updates compared to the database
    returns 4 variables!!! 2 boolean, 1 sid str, 1 msg str
    BE AWARE THAT NOW I AM USING A SIMPLE VARIABLE FAKE USER_DATA
    NEED TO UPDATE Tomorrow
    also we need a separate function that just update database
    """
    # get a list of conversations from our chat service
    conversations = client.conversations.v1.services(a_chat_service_sid).conversations.list()
    new_user = False
    new_msg = False

    # condition_1: new user, new conversation id
    if len(conversations) > len(user_data):
        for conversation in conversations:
            if conversation.sid not in user_data:
                print("New conversation detected:", conversation.sid)
                new_user = True
                new_msg = True
                latest_msg = conversation.messages.list()[-1].body.title()
                return new_user, new_msg, conversation.sid, latest_msg

    # condition_2: same users, then loop to see whether there's new msg
    elif len(conversations) == len(user_data):
        for conversation in conversations:
            total_msg_num = len(conversation.messages.list())
            record_msg_num = user_data[conversation.sid]["Total number of msg"]
            if total_msg_num > record_msg_num:
                new_msg = True
                latest_msg = conversation.messages.list()[-1].body.title()
                if latest_msg != user_data[conversation.sid]["Last message"]:
                    user_data[conversation.sid]["Last message"] = latest_msg
                    print("New message detected:", conversation.sid, latest_msg)
                    return new_user, new_msg, conversation.sid, latest_msg
            else:
                return

    # condition_3: deleted conversation detected, then remove it from database
    else:
        conversations_lst = []
        for conversation in conversations:
            conversations_lst.append(conversation.sid)
        for user_sid in user_data:
            if user_sid not in conversations_lst:
                del user_data[user_sid]
                print("A conversation was gone, we remove it from our database too")
                return


def list_conversations(a_chat_service_sid):
    """
    lists conversations from Twilio in a specific chat service
    """
    conversations = client.conversations.v1.services(a_chat_service_sid).conversations.list()

    for conversation in conversations:
        conver_length = len(conversation.messages.list())
        print(f"Conversation SID: {conversation.sid}, Conversation status: {conversation.state}, Total messages: {conver_length}",
              {conversation.friendly_name})
# list_conversations(chat_service_sid)


def get_user_whatsapp_via_friendly_name(a_conversation_sid):
    conversation = client.conversations.v1.services(chat_service_sid).conversations(a_conversation_sid).fetch()
    friendly_name = conversation.friendly_name.split(" ")
    detected_whatsapp = friendly_name[1].strip()
    return detected_whatsapp
# print(get_user_whatsapp_via_friendly_name(programmer_conversation_sid))

# def keep_simple_polling_and_react(a_chat_service_sid, interval):
#     """
#     keeps running with a time interval
#     """
#     print(f"Monitoring Conversations: {a_chat_service_sid}")
#     while True:
#         new_conversation_info = detect_new_incoming_msg(chat_service_sid, user_data_just_a_demo)
#         if new_conversation_info:
#             new_user, new_msg, conver_id, latest_msg = new_conversation_info
#             if conver_id != "" and latest_msg != "":
#                 return conver_id, latest_msg
#         print(datetime.datetime.now())
#         time.sleep(interval) # take a break, int seconds


# what do we need in the database???
user_data_just_a_demo = {
    "CH8832e427c1d646daa19fdd10181185c3":
        {"Conversation Friendly Name": "RunOutOfSnacks",
         "Last message": "Bye",
         "Total number of msg": 21,
         },
    "CH49209d41e3604a9b85598ebb7f4ecd65":
        {"Conversation Friendly Name": "RandomFriendlyName",
         "Last message": "Bye", "Total number of msg": 2,
         },
    "CHa5e5424de3874cf8bb2205ddf64e25d9":
        {"Conversation Friendly Name": "RunOutOfSnacks",
         "Last message": "Bye", "Total number of msg": 3,
         },
    "CH0e1b7455098a4828a3c9cfba68565132":
        {"Conversation Friendly Name": "RunOutOfSnackssnacks",
         "Last message": "Bye", "Total number of msg": 12,
         },
    "CH490cf1c182714b6db91d90a9976797b9":
        {"Conversation Friendly Name": "RunOutOfSnackssnacks",
         "Last message": "Bye", "Total number of msg": 8,
         },
}


# keep_simple_polling(chat_service_sid, 5)