from services import twilio_service as twilio
from services.utility import welcome_user

while True:
    chat_ids = twilio.get_conversation_sids()
    print(chat_ids)

    for chat_id in chat_ids:
        print(chat_id)
        #welcome_user(chat_id) # --> this should send a welcome message
        # and: save new user to database! create save method and call it where?
        twilio.send_follow_up_message(chat_id, "Dudidudidudidudi", )
        latest_message = twilio.retrieve_latest_message()

        print(latest_message)

        break

