"""
Using APIs to get Memes
"""

import os
import requests
import datetime
import random
import praw
from dotenv import load_dotenv


from ai.openai_helper import get_text_response_from_openai


REDDIT_MEME_URL = "https://www.reddit.com/r/memes/top/.json"
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
user_number = os.getenv("USER_PHONE_NUMBER")

# Set up Reddit API using PRAW
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="whatsmeme-script"
)


def get_top_meme_of_the_time(time): # "week"
    """
    get the top meme of a given time
    day, week, month, year
    """
    url = REDDIT_MEME_URL
    params = {
        "t": time,  # time range
        "limit": 1    # top 1 post
    }
    headers = {
        "User-Agent": "Mozilla/5.0"  # Reddit requires a User-Agent header
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # get the top post from the data
    top_post = data['data']['children'][0]['data']
    # meme info
    title = top_post['title']
    image_url = top_post.get('url_overridden_by_dest', 'No image')
    permalink = f"https://reddit.com{top_post['permalink']}"

    text = f"Hohoho, as of today, {datetime.datetime.today().date()}, the top meme of the {time} is: {title}"
    return text, image_url, permalink


def get_top_meme_of_the_day():
    return get_top_meme_of_the_time("day")


def get_top_meme_of_the_week():
    return get_top_meme_of_the_time("week")


def get_top_meme_of_the_month():
    return get_top_meme_of_the_time("month")


def get_top_meme_of_the_year():
    return get_top_meme_of_the_time("year")


def get_random_meme():
    # Use PRAW to get a random meme from the memes subreddit
    memes = list(reddit.subreddit("memes").hot(limit=50))  # Get the top 50 hot posts
    meme = memes[random.randint(0, len(memes) - 1)]  # Select a random meme

    title = meme.title
    image_url = meme.url
    permalink = f"https://reddit.com{meme.permalink}"

    return title, image_url, permalink


def get_ai_response_to_meme_title(meme_text):
    """
    ai receives text and return response
    """
    print(get_text_response_from_openai(meme_text))
    print(type(get_text_response_from_openai(meme_text)))
    return get_text_response_from_openai(meme_text)


def send_meme_via_whatsapp(from_whatsapp, to_whatsapp):
    from services.twilio_service import send_msg_with_media

    meme_info = get_top_meme_of_the_day()
    meme_text = meme_info[0]
    ai_comment = get_ai_response_to_meme_title(meme_text + "Please respond in 1 or 2 short sentences.")
    body = meme_text + "\n\n" + ai_comment
    media_url = meme_info[1]
    send_msg_with_media(from_whatsapp, to_whatsapp, body, media_url)


def send_random_meme_via_whatsapp(from_whatsapp, to_whatsapp):
    from services.twilio_service import send_msg_with_media

    meme_info = get_random_meme()
    meme_text = meme_info[0]
    ai_comment = get_ai_response_to_meme_title(meme_text + "Please respond in 1 or 2 short sentences.")
    body = meme_text + "\n\n" + ai_comment
    media_url = meme_info[1]
    send_msg_with_media(from_whatsapp, to_whatsapp, body, media_url)