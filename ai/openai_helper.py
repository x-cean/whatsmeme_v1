import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPEN_AI_KEY")

def get_generated_meme_from_openai(prompt):
    try:
        response = openai.Image.create(prompt=prompt, n=1, size="512x512")
        print(response)
        meme_url = response['data'][0]['url']
        return meme_url
    except openai.OpenAIError as e:
        print(f"An error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None





