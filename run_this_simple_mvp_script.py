from dotenv import load_dotenv
from ai.openai_helper import get_generated_meme_from_openai, get_text_response_from_openai
from services.twilio_service import get_conversation_sids, send_msg_with_media, send_text_message, retrieve_latest_message, detect_new_incoming_msg, get_user_whatsapp_via_friendly_name
from services.utility import welcome_user
from reddit_meme import send_meme_via_whatsapp, send_random_meme_via_whatsapp
from data.json_data_manager import load_users, add_user, update_user, save_users
import os
import datetime
import time

load_dotenv()

account_sid = os.getenv("MS_TWILIO_ACCOUNT_SID")
api_sid = os.getenv("MS_TWILIO_API_KEY_SID")
api_secret = os.getenv("MS_TWILIO_API_KEY_SECRET")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
user_number = os.getenv("USER_PHONE_NUMBER")
chat_service_sid = os.getenv("CHAT_SERVICE_SID")


# get friendly name
# get name
# number of msg

def main_mvp_script():
    # create a while loop with 5s time breaks
    is_first_message = True
    print(f"Monitoring Conversations: {chat_service_sid}")
    while True:
        user_data = load_users()
        new_conversation_info = detect_new_incoming_msg(chat_service_sid, user_data)
        if new_conversation_info:
            is_new_user, is_new_msg, conver_id, latest_msg, number_of_msg = new_conversation_info
            new_to_whatsapp = get_user_whatsapp_via_friendly_name(conver_id)
            print(new_to_whatsapp, type(new_to_whatsapp))
            if is_new_msg:
                if is_first_message:
                    send_text_message(new_to_whatsapp, "Heyo! You got the first message of our today's run!")
                    is_first_message = False
                if is_new_user:
                    #to_whatsapp =
                    #welcome_new_user()
                    # for now this is specific for new user
                    send_text_message(new_to_whatsapp,
                                      "Welcome to WhatsMEME – great that you found us! We love to share memes and happiness!")
                    add_user(conver_id, {"name": "SPACEHOLDER"})
                if conver_id != "" and latest_msg != "":
                    # send_text_message(new_to_whatsapp, "Do you want the meme of the day? Type '1'! Or do you want to generate a meme? Type '2'")
                    first_reply_to_new_msg = get_text_response_from_openai(
                        latest_msg + "Respond in 2 to 3 sentences, then say sth like 'I want to share something to make it a better day for you!' but change the quote slightly")
                    send_text_message(new_to_whatsapp, first_reply_to_new_msg)
                    send_random_meme_via_whatsapp(twilio_number, new_to_whatsapp)
                    update_user(conver_id, {"latest_message": latest_msg, "total_number_of_msg": number_of_msg})

        print(datetime.datetime.now())
        time.sleep(5)  # take a break, int seconds


def backup_main_mvp():
    """
    when this is running, it detects new incoming msg
    if found, will answer it (with ai), and share a top meme of the day
    NEED further development:
    1. need to restructure a lot, so that the responding can happen inside a while loop, then keep on looping,
    now it stops because I used return to make this fast demo
    2. of course updating database is key to let it work, currently just using a fixed database in this demo
    3. need to keep the conversation going back and forth
    """
    pass
    # new_msg_info = keep_simple_polling(chat_service_sid, 5)
    # if new_msg_info:
    #     sid = new_msg_info[0]
    #     msg = new_msg_info[1]
    #     first_reply_to_new_msg = get_text_response_from_openai(msg + "Respond in 2 to 3 sentences, then say sth like 'I want to share something to make it a better day for you!' but change the quote slightly")
    #     send_text_message(first_reply_to_new_msg)
    #     send_meme_via_whatsapp(twilio_number, user_number)


if __name__ == "__main__":
    main_mvp_script()