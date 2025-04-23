
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

load_dotenv()

def get_generated_meme_from_openai(prompt):
    try:
        client = OpenAI()
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        image_url = response.data[0].url
        print(image_url)
        return image_url

    except OpenAIError as e:
        print(f"An OpenAI error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_text_response_from_openai(prompt):
    try:
        client = OpenAI()
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


# print(get_generated_meme_from_openai("please create a meme for me, using any well-known meme template"))
# get_text_response_from_openai("wow wow wow who is here")