#hello - elinor
#hi - Xiao
#just another test - X

from ai import openai_helper as ai
from data.datamanager import send_message

prompt = "create a cat meme, please. it should be cute"

meme_url = ai.get_generated_meme_from_openai(prompt)
if meme_url:
    send_message(meme_url)