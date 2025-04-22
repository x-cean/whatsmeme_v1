import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPEN_AI_KEY")


def get_generated_meme_from_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt}
            ]
        )
        print(response)

        #TODO image generation - does that work with the model we have a key for?

    except openai.OpenAIError as e:
        print(f"An error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None





