from dotenv import load_dotenv
from ai.openai_helper import get_generated_meme_from_openai
from services.twilio_service import get_conversation_sids, send_msg_with_media, send_text_message, retrieve_latest_message
from services.utility import welcome_user
from reddit_meme import send_meme_via_whatsapp
import os

load_dotenv()

twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
user_number = os.getenv("USER_PHONE_NUMBER")



while True:
    chat_ids = get_conversation_sids()
    print(chat_ids)


    for chat_id in chat_ids:
        print(chat_id)
        #welcome_user(chat_id) this should send a welcome message based on whether the user already exists

        send_meme_via_whatsapp(twilio_number, user_number) #sends top meme of the day

        latest_messages = retrieve_latest_message()




        if latest_messages:
            if latest_messages[0] == 1:
                # random meme will be picked and sent
                pass
            elif latest_messages[0] == 2:
                # choosing a topic for the meme, fitting meme will be sent
                pass
            elif latest_messages[0] == 3:
                send_text_message("What kind of meme should it be? Give me a short description!")
                while True:
                    latest_messages = retrieve_latest_message()
                    if latest_messages[0] == 3:
                        continue
                    prompt = latest_messages[0]
                    send_msg_with_media(twilio_number, user_number, "Here is your AI generated picture!", get_generated_meme_from_openai(prompt))
                    break





