import os
import openai
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

load_dotenv()



def get_generated_meme_from_openai(prompt):
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "can you create a cat image for me?"}
            ]
        )
        print(response.choices[0].message.content)

        # response = client.images.generate(
        #     model="dall-e-3",
        #     prompt=prompt,
        #     n=1,
        #     size="1024x1024",
        #     quality="standard",
        # )
        # print(response)
        # image_url = response.data[0].url
        # print("Image URL:", image_url)
        # return image_url
    except OpenAIError as e:
        print(f"An OpenAI error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

get_generated_meme_from_openai("a cute cat picture")