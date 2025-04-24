from dotenv import load_dotenv
from ai.openai_helper import get_generated_meme_from_openai, get_text_response_from_openai
from services.twilio_service import get_conversation_sids, send_msg_with_media, send_text_message, retrieve_latest_message, detect_new_incoming_msg, user_data_just_a_demo
from services.utility import welcome_user
from reddit_meme import send_meme_via_whatsapp
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


def main_mvp_script():
    # create a while loop with 5s time breaks
    print(f"Monitoring Conversations: {chat_service_sid}")
    while True:
        new_conversation_info = detect_new_incoming_msg(chat_service_sid, user_data_just_a_demo)
        if new_conversation_info:
            new_user, new_msg, conver_id, latest_msg = new_conversation_info
            if new_msg:
                if new_user:
                    pass # welcome and get user name
                if conver_id != "" and latest_msg != "":
                    first_reply_to_new_msg = get_text_response_from_openai(
                        latest_msg + "Respond in 2 to 3 sentences, then say sth like 'I want to share something to make it a better day for you!' but change the quote slightly")
                    send_text_message(first_reply_to_new_msg)
                    send_meme_via_whatsapp(twilio_number, user_number)
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