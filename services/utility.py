import json
import os
import random


def load_users():
    """
    Loads user data from the 'users.json' file.
    Creates an empty file if it does not exist.
    """
    if not os.path.exists("data/user_data.json"):
        with open("data/user_data.json", "w") as file:
            json.dump({}, file)
    with open("data/user_data.json", "r") as handle:
        return json.load(handle)


def save_users(data):
    with open("data/user_data.json", "w") as file:
        json.dump(data, file, indent=4)


def is_new_user(user_id, name=None):
    """Checks if the user_id is already registered.
    If new, initializes the user's data.
    Args:
        user_id (str): Unique ID (Conversation_ID)
        name (str, optional): The user's name if it's a new user.
    Returns:
        bool: True if user is new, False if already registered."""
    users = load_users()

    if user_id in users:
        return False
    else:
        users[user_id] = {
            "name": name if name else "Unknown",
            "seen_memes": [],
            "last_meme": None
        }
        save_users(users)
        return True


def welcome_user(user_id):
    """
    Greets the user based on whether they are new or returning.
    For new users, prompts for their name and stores it.
    """
    users = load_users()

    if user_id in users:
        name = users[user_id].get("name", "friend")
        print(f"\nWelcome back, {name}! Ready for some fresh laughs?")
    else:
        print("Hi there! Welcome to WhatsMEME – A place to lighten up your mood with some funny memes!\n")
        name = input("Before we start, what’s your name? ").strip()

        users[user_id] = {
            "name": name,
            "seen_memes": [],
            "last_meme": None
        }
        save_users(users)

        print(f"\nNice to meet you, {name}!")
        print("Let’s dive into some hilarious content!")

    return name


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
    print("2 - Choose a meme by topic or mood:")
    print("    Feeling something specific? Just tell us your vibe – like 'cats', 'work', or 'weekend' – and we’ll match a meme to it.")
    print("3 - Generate your own meme:")
    print("    Be the meme-maker! Describe your ideal meme and add your own caption.")
    print("'help' - View this menu anytime.")
    print("'exit' - Leave WhatsMEME (but come back soon for more laughs!)\n")


def get_random_meme(user_name):
    """Fetches and displays a random meme from an external API.
    Stores the meme in the user's seen history.
    Args:
        user_name (str): The name of the current user."""
    
    if user_name not in user_db:
        user_db[user_name] = {"seen_memes": []}

    seen = user_db[user_name]["seen_memes"]
    unseen_memes = [meme for meme in meme_bank if meme not in seen]

    if not unseen_memes:
        print("😅 Uh-oh! You’ve seen all our memes for now.")
        print("Check back later when we've got more meme madness for you!")
        return

    selected_meme = random.choice(unseen_memes)
    user_db[user_name]["seen_memes"].append(selected_meme)

    print("\nHere's your random meme! 😂")
    print(f"{selected_meme}")


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
