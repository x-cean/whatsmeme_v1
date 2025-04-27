import json
import os
import random
from data.json_data_manager import load_users, add_user, save_users
from services.twilio_service import send_text_message


def welcome_new_user(to_whatsapp):
    message = "Hi there! Welcome to WhatsMEME – A place to lighten up your mood with some funny memes! 😄 Before we start, what's your name?"
    send_text_message(to_whatsapp, message)
    name = input().strip()
    message = f"Nice to meet you, {name}! Let's dive into some hilarious content!"
    send_text_message(to_whatsapp, message)
    return name

def welcome_existing_user(to_whatsapp, name):
    message = f"Welcome back, {name}!"


def welcome_user(chat_id):
    """
    Greets the user based on whether they are new or returning.
    For new users, prompts for their name and stores it.
    Returns the welcome message to be sent via WhatsApp.
    """

    #TODO send request for name if the user is new. accept the next message and assign it to name

    users = load_users()
    chat_id = str(chat_id)
    if chat_id in users.keys():
        name = users[chat_id].get("name", "friend")
        message = f"Welcome back, {name}! Ready for some fresh laughs? 😂"
    else:
        # New user flow
        message = "Hi there! Welcome to WhatsMEME – A place to lighten up your mood with some funny memes! 😄\n"
        name = input("Before we start, what’s your name? ").strip()

        users[chat_id] = {
            "name": name,
            "conversation_friendly_name": "",
            "last_message": "",
            "total_number_of_msg": ""
        }
        save_users(users)

        message += f"\nNice to meet you, {name}!\nLet’s dive into some hilarious content!"

    return message, name

def display_menu():
    print("\nWould you like to explore some more hilarious memes?")
    print("Here is how I can help you today! Just make a choice:")
    print("1 - Get a random meme")
    print("2 - Choose a meme based on a topic or mood")
    print("3 - Generate your own meme")
    print("Type 'help' to get indepth explanations of the various choices and 'exit' to quit.")


def show_help_menu():
    """Displays help instructions for navigating the WhatsMEME app.
    Explains how to choose options and use the available features."""
    print("\n--- WhatsMEME Help Menu ---")
    print("Here's a quick guide to brighten your day with memes:")
    print("1 - Get a random meme:")
    print("    We'll surprise you with a meme from our hilarious collection.")
    #print("2 - Choose a meme by topic or mood:")
    #print("    Feeling something specific? Just tell us your vibe – like 'cats', 'work', or 'weekend' – and we’ll match a meme to it.")
    print("3 - Generate your own meme:")
    print("    Be the meme-maker! Describe your ideal meme and add your own caption.")
    print("'help' - View this menu anytime.")
    print("'exit' - Leave WhatsMEME (but come back soon for more laughs!)\n")



def get_meme_by_topic(user_name, topic):
    """Fetches and displays a meme related to a specific topic or mood.
    Updates the user's meme history.
    Args:
        user_name (str): The name of the current user.
        topic (str): The keyword/topic for the meme search."""
    pass


def generate_custom_meme(user_name, template_description, text):
    """Uses AI to create a custom meme
    based on the user’s template description and caption/text.
    Args:
        user_name (str): The name of the current user.
        template_description (str): A description of the desired meme template.
        text (str): Caption or content for the meme."""
    pass
