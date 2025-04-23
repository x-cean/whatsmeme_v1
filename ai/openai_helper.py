import os

from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY_IMAGE = os.getenv("OPENAI_API_KEY_IMAGE")
OPENAI_API_KEY_CHAT = os.getenv("OPENAI_API_KEY_CHAT")


def get_generated_meme_from_openai(prompt):
    """prompts dall-e-2 to create an image, using the prompt that has been sent in via arguments.
    the function will return the url of the created image as a string"""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY_IMAGE)
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        image_url = response.data[0].url
        return image_url

    except OpenAIError as e:
        print(f"An OpenAI error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_text_response_from_openai(prompt):
    """asks gpt-4o-mini for a textual response to a prompt that has been sent in
    via the arguments. returns the textual response as a string"""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY_CHAT)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except OpenAIError as e:
        print(f"An OpenAI error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


# (get_generated_meme_from_openai("please create a picture of an apple tree"))
# get_text_response_from_openai("wow wow wow who is here")