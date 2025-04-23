from ai import openai_helper as ai
from services.twilio_service import send_message
from services.utility import welcome_user

while True:
    #loop through all conversations - conversation sid for looping
    send_message("Hello, this is a test")
    break

