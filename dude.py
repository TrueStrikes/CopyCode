import requests
import json
import os
import time
import threading
import re
import pygame
import colorama
import clipboard

# Initialize colorama
colorama.init()

# Set to keep track of retrieved message IDs and user messages
retrieved_message_ids = set()
user_messages = set()

# Variable to indicate if the script is running
running = True

def display_message(channelid, message):
    message_id = message.get('id')
    if message_id not in retrieved_message_ids:
        retrieved_message_ids.add(message_id)
        author_id = message.get('author', {}).get('id')
        content = message.get('content')
        if author_id in target_user_ids and content not in user_messages:
            print(colorama.Fore.YELLOW + "Message:")
            print(content)
            print(colorama.Style.RESET_ALL)

            # Check if the content starts with "# "
            if content.startswith("# "):
                content = content[2:]  # Remove "# " from the beginning

            copy_to_clipboard(content)  # Copy the message content to the clipboard
            user_messages.add(content)
            play_sound("t.mp3")  # Play the sound "t.mp3"

def retrieve_latest_messages(channelid):
    headers = {
        'authorization': bot_token
    }
    params = {
        'limit': 1  # Update to retrieve the last 5 messages
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
        pygame.mixer.init()
        pygame.mixer.music.load(sound_filename)
        pygame.mixer.music.play()
        time.sleep(1)  # Give it some time to play the sound
    except Exception as e:
        print("Error playing sound:", e)

# Copy the message content to the clipboard
def copy_to_clipboard(content):
    clipboard.copy(content)

# Clear the console and print "Watching" in bright yellow
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(colorama.Fore.YELLOW + "Watching")
    print(colorama.Style.RESET_ALL)

# Call the function to clear the console and print "Watching"
clear_console()

# Read the filename of the JSON file from config.json
config_filename = "config.json"
try:
    with open(config_filename, 'r') as config_file:
        config_data = json.load(config_file)
except (FileNotFoundError, json.JSONDecodeError):
    config_data = {}  # If there's an error or the file doesn't exist, initialize an empty config dictionary

# Load the settings from the specified file
settings_filename = config_data.get("config_filename", "settings.json")
try:
    with open(settings_filename, 'r') as settings_file:
        settings_data = json.load(settings_file)
        bot_token = settings_data.get("bot_token", "")
        target_user_ids = settings_data.get("target_user_ids", [])
        target_channels = settings_data.get("target_channels", [])
except (FileNotFoundError, json.JSONDecodeError):
    bot_token = ""
    target_user_ids = []
    target_channels = []

# Set the loop to run indefinitely
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

    time.sleep(0.05)  # Add a wait time of 0.2 seconds before the next iteration
