import requests
import json
import os
import time
import threading
import re
import colorama
import clipboard
import keyboard
from playsound import playsound

# Initialize colorama
colorama.init()

# Set to keep track of retrieved message IDs and user messages
retrieved_message_ids = set()
user_messages = set()

# Variable to indicate if the script is running
running = True

def extract_code_from_embed(embed):
    code_pattern = r"\*\*Code\*\*: ([^\n]+)"
    match = re.search(code_pattern, embed.get('description', ''))
    if match:
        return match.group(1)
    return None

def display_message(channelid, message):
    message_id = message.get('id')
    if message_id not in retrieved_message_ids:
        retrieved_message_ids.add(message_id)
        author_id = message.get('author', {}).get('id')
        content = message.get('content')

        embeds = message.get('embeds', [])
        if embeds:
            print(colorama.Fore.YELLOW + "Message with Embeds:")
            print(content)
            code_found = False
            for embed in embeds:
                code = extract_code_from_embed(embed)
                if code:
                    print(f"Code: {code}")
                    copy_to_clipboard(code)
                    user_messages.add(code)
                    code_found = True
            if code_found:
                print("Code found in this message.")
                play_sound("t.mp3")
            else:
                print("No code found in this message.")
            print(colorama.Style.RESET_ALL)
        else:
            if author_id in target_user_ids and content not in user_messages:
                print(colorama.Fore.YELLOW + "Message:")
                print(content)
                print(colorama.Style.RESET_ALL)

                if content.startswith("# "):
                    content = content[2:]

                copy_to_clipboard(content)
                user_messages.add(content)

                if auto_enter_mode:
                    perform_auto_enter()
                else:
                    print("No code found in this message.")

def retrieve_latest_messages(channelid):
    headers = {
        'authorization': bot_token
    }
    params = {
        'limit': 1
    }
    r = requests.get(f'https://discord.com/api/v8/channels/{channelid}/messages', headers=headers, params=params)
    try:
        messages = json.loads(r.text)
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        return []

    if not isinstance(messages, list) or len(messages) == 0:
        return []

    return messages

def play_sound(sound_filename):
    try:
        playsound(sound_filename)
        time.sleep(1)
    except Exception as e:
        print("Error playing sound:", e)

def copy_to_clipboard(content):
    clipboard.copy(content)

config_filename = "config.json"
try:
    with open(config_filename, 'r') as config_file:
        config_data = json.load(config_file)
except (FileNotFoundError, json.JSONDecodeError):
    config_data = {}

settings_filename = config_data.get("config_filename", "settings.json")
try:
    with open(settings_filename, 'r') as settings_file:
        settings_data = json.load(settings_file)
        bot_token = settings_data.get("bot_token", "")
        target_user_ids = settings_data.get("target_user_ids", [])
        target_channels = settings_data.get("target_channels", [])
        auto_enter_mode = settings_data.get("auto_enter_mode", False)
except (FileNotFoundError, json.JSONDecodeError):
    bot_token = ""
    target_user_ids = []
    target_channels = []
    auto_enter_mode = False

while True:
    if running and bot_token and target_user_ids and target_channels:
        headers = {
            'authorization': bot_token
        }

        for channel_id in target_channels:
            latest_messages = retrieve_latest_messages(channel_id)
            if latest_messages:
                for message in latest_messages:
                    display_message(channel_id, message)

    time.sleep(0.05)
