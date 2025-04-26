from dotenv import load_dotenv
from ai.openai_helper import get_generated_meme_from_openai, get_text_response_from_openai
from services.twilio_service import get_conversation_sids, send_msg_with_media, send_text_message, retrieve_latest_message, detect_new_incoming_msg, get_user_whatsapp_via_friendly_name
from services.utility import welcome_user
from reddit_meme import send_meme_via_whatsapp, send_random_meme_via_whatsapp, get_top_meme_of_the_day, get_top_meme_of_the_month, get_top_meme_of_the_week, send_top_meme_week_via_whatsapp, send_top_meme_month_via_whatsapp
from data.json_data_manager import load_users, add_user, update_user, save_users
import os
import datetime
import time
import random

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

def make_meme_and_send_via_whatsapp(from_whatsapp, to_whatsapp, prompt):
    send_text_message(to_whatsapp, "Generating your meme picture, please wait...")
    send_msg_with_media(from_whatsapp, to_whatsapp, "Here is your picture!", get_generated_meme_from_openai(prompt))


def send_a_menu(to_whatsapp):
    send_text_message(to_whatsapp, "here is a glimpse of what we can do: \n* Type '000' to call out this menu again! \n\n* Type '001' for meme of the day! \n\n* Type '002' for meme of the week! \n\n* Type '003' for meme of the month! \n\n* Hola! Type '007' for AI freshly made meme! (And we don't know what is in their mind, right?)")


def lottery_nr():
    return random.randint(1, 3)


def main_mvp_script():
    # create a while loop with 2s time breaks
    is_first_message = True
    print(f"Monitoring Conversations: {chat_service_sid}")
    while True:
        user_data = load_users()
        new_conversation_info = detect_new_incoming_msg(chat_service_sid, user_data)
        if new_conversation_info:
            is_new_user, is_new_msg, conver_id, latest_msg, number_of_msg = new_conversation_info
            new_to_whatsapp = get_user_whatsapp_via_friendly_name(conver_id)
            print(new_to_whatsapp, type(new_to_whatsapp)) # just for backend monitoring
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
                    send_a_menu(new_to_whatsapp)
                    add_user(conver_id, {"name": "SPACEHOLDER"})
                if conver_id != "" and latest_msg != "":
                    # lots of options
                    if latest_msg.strip() == "000":
                        send_a_menu(new_to_whatsapp)
                    elif latest_msg.strip() == "001":
                        send_meme_via_whatsapp(twilio_number, new_to_whatsapp)
                        send_a_menu(new_to_whatsapp)
                    elif latest_msg.strip() == "002":
                        send_top_meme_week_via_whatsapp(twilio_number, new_to_whatsapp)
                        send_a_menu(new_to_whatsapp)
                    elif latest_msg.strip() == "003":
                        send_top_meme_month_via_whatsapp(twilio_number, new_to_whatsapp)
                        send_a_menu(new_to_whatsapp)
                    elif latest_msg.strip() == "007":
                        text = "A grumpy cat sitting at a computer desk, wearing glasses, surrounded by coffee cups and messy paperwork, looking completely done with life. The background is a chaotic home office. The scene is cartoonish with exaggerated facial expressions, in the style of a relatable internet meme. With the meme written in the picture in an obvious way."
                        make_meme_and_send_via_whatsapp(twilio_number, new_to_whatsapp, text)
                        send_text_message(new_to_whatsapp, "There's more we can do! \nIf you want to generate a meme with your own description, please start your msg with '007' followed by your description! We (and our AI fellow) will give it our best try!")
                    elif len(latest_msg.strip()) > 5 and latest_msg.strip()[:3] == "007":
                        make_meme_and_send_via_whatsapp(twilio_number, new_to_whatsapp, latest_msg[4:])
                        send_a_menu(new_to_whatsapp)
                    else:
                        first_reply_to_new_msg = get_text_response_from_openai(
                            latest_msg + "Respond in 2 short sentences, then say sth like 'I want to share something to make it a better day for you!', change the quote but means the same, or similar")
                        send_text_message(new_to_whatsapp, first_reply_to_new_msg)
                        send_random_meme_via_whatsapp(twilio_number, new_to_whatsapp)
                        random_number = lottery_nr()
                        if is_new_user:
                            random_number == 3
                        if random_number == 1:
                            send_text_message(new_to_whatsapp, "By the way")
                            send_a_menu(new_to_whatsapp)

                    # here can add the drop-down menu

                    update_user(conver_id, {"latest_message": latest_msg, "total_number_of_msg": number_of_msg})

        print(datetime.datetime.now())
        time.sleep(2)  # take a break, int seconds


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