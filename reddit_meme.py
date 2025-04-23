"""
Using APIs to get Memes
"""

import os
import requests
import datetime
from dotenv import load_dotenv

from services.twilio_service import send_msg_with_media
from ai.openai_helper import get_generated_meme_from_openai


REDDIT_MEME_URL = "https://www.reddit.com/r/memes/top/.json"
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
user_number = os.getenv("USER_PHONE_NUMBER")


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

    text = f"Hohoho, as of today {datetime.datetime.today().date()}, the top meme of the {time} is: {title}"
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
    pass
    # feasible, need a reddit developer account, will take care of this later


def get_AI_response_to_meme_title(meme_text):



def send_meme_via_whatsapp(from_whatsapp, to_whatsapp):
    meme_info = get_top_meme_of_the_month()
    body = meme_info[0]
    media_url = meme_info[1]
    send_msg_with_media(from_whatsapp, to_whatsapp, body, media_url)


send_meme_via_whatsapp(twilio_number, user_number)