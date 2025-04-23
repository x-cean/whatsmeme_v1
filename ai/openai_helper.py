import os
import openai
from openai import OpenAIError
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPEN_AI_KEY")

def get_generated_meme_from_openai(prompt):
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="standard",
            response_format="url"
        )
        print(response)
        image_url = response.data[0].url
        print("Image URL:", image_url)
        return image_url
    except OpenAIError as e:
        print(f"An OpenAI error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

get_generated_meme_from_openai("a cute cat picture")





