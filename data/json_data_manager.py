import json
from json import JSONDecodeError


def load_users():
    """Loads user data from the 'user_data.json' file and returns it.
    Creates and returns an empty file if it does not exist."""
    try:
        with open("user_data.json") as handle:
            data = json.load(handle)
            return data
    except (FileNotFoundError, JSONDecodeError):
        with open("user_data.json", "w") as handle:
            json.dump({}, handle)
        return {}


def add_user(chat_id, new_user):
    """adds user with a specific chat id. user should be sent in as a dictionary"""
    data = load_users()
    chat_id = str(chat_id)
    chat_ids_list = data.keys()
    print(chat_ids_list)
    if chat_id in chat_ids_list:
        print("this user already exists!")
        return

    data[chat_id] = new_user
    save_users(data)


def update_user(chat_id, updated_user_info):
    """updates an existing user with a specific chat_id. note: the user is not
    replaced with the new info, instead we are calling update. that enables
    partial updating but it means that old key-value pairs wont be removed"""
    data = load_users()
    chat_id = str(chat_id)
    chat_ids_list = data.keys()
    if chat_id in chat_ids_list:
        data[chat_id].update(updated_user_info)
        save_users(data)
    else:
        print("this user doesn't exist!")


def save_users(data):
    """overwrites the data in our json file with the new data sent in via arguments"""
    with open("user_data.json", "w") as handle:
        json.dump(data, handle, indent=4)
    print("saved successfully!")