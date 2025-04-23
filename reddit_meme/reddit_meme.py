"""
Using APIs to get Memes
"""


import requests
import datetime


REDDIT_MEME_URL = "https://www.reddit.com/r/memes/top/.json"


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


get_top_meme_of_the_day()
def send_meme_via_whatsapp(from_whatsapp, to_whatsapp):
    meme_info = get_top_meme_of_the_month()
    body = meme_info[0]
    media_url = meme_info[1]
    send_msg_with_media(from_whatsapp, to_whatsapp, body, media_url)
