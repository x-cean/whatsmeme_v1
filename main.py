from ai import openai_helper as ai
from services.twilio_service import send_message

prompt = "create a funny meme with cats, please. it should be cute"

meme_url = ai.get_generated_meme_from_openai(prompt)
if meme_url:
    send_message(meme_url)
