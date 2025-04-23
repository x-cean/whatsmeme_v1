def is_new_user(name):
    """Checks whether the user is new or returning.
    Adds the user to the system if they don't exist.
    Args:
        name (str): The username to check.
    Returns:
        bool: True if the user is new, False otherwise."""
    pass

def welcome_user():
    """Greets the user, asks for their name, and identifies whether they are new or returning.
        Provides a custom welcome message based on that.
        Returns:
            str: The name of the user."""

    print("Hi there! Welcome to WhatsMEME – A place to lighten up your mood with some funny memes!\n")
    name = input("Before we start, what’s your name? ").strip()

    if is_new_user(name):
        print(f"\nNice to meet you, {name}!")
        print(f"Let’s dive into some hilarious content!")
    else:
        print(f"\nWelcome back, {name}! Ready for some fresh laughs?")

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
    pass


def get_random_meme(user_name):
    """Fetches and displays a random meme from an external API.
    Stores the meme in the user's seen history.
    Args:
        user_name (str): The name of the current user."""
    pass


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