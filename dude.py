import requests
import json
import os
import time
import threading
import re
import pygame
import colorama
import clipboard
import keyboard
import pyautogui

# Initialize colorama
colorama.init()

# Set to keep track of retrieved message IDs and user messages
retrieved_message_ids = set()
user_messages = set()

# Variable to indicate if the script is running
running = True

# Function to save auto click redeem coordinates to a file
def save_auto_redeem_coordinates(x, y):
    with open("auto_redeem_coordinates.txt", "w") as f:
        f.write(f"{x},{y}")

# Function to load auto click redeem coordinates from a file
def load_auto_redeem_coordinates():
    try:
        with open("auto_redeem_coordinates.txt", "r") as f:
            coordinates = f.read().strip().split(',')
            if len(coordinates) == 2:
                return int(coordinates[0]), int(coordinates[1])
    except (FileNotFoundError, ValueError):
        pass
    return None

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
        auto_enter_mode = settings_data.get("auto_enter_mode", False)
        auto_click_mode = settings_data.get("auto_click_mode", False)
except (FileNotFoundError, json.JSONDecodeError):
    bot_token = ""
    target_user_ids = []
    target_channels = []
    auto_enter_mode = False
    auto_click_mode = False

# Check if auto redeem mode is enabled
auto_redeem_coordinates = None

if auto_click_mode:
    existing_coordinates = load_auto_redeem_coordinates()

    if existing_coordinates:
        use_existing = input(f"Auto redeem mode is enabled. Do you want to use existing coordinates {existing_coordinates}? (y/n): ")
        if use_existing.lower() == 'y':
            auto_redeem_coordinates = existing_coordinates
        else:
            print("Please click where you want to save the new auto click redeem coordinates. (Keep your mouse there for about 6 seconds)")
            time.sleep(4)  # Give the user time to switch to the desired location

            # Get and save the mouse coordinates
            auto_redeem_coordinates = pyautogui.position()
            save_auto_redeem_coordinates(auto_redeem_coordinates[0], auto_redeem_coordinates[1])
            print(f"New auto click redeem coordinates saved: {auto_redeem_coordinates}")
    else:
        print("Auto redeem mode is enabled. Please click where you want to save the auto click redeem coordinates.")
        time.sleep(2)  # Give the user time to switch to the desired location

        # Get and save the mouse coordinates
        auto_redeem_coordinates = pyautogui.position()
        save_auto_redeem_coordinates(auto_redeem_coordinates[0], auto_redeem_coordinates[1])
        print(f"Auto click redeem coordinates saved: {auto_redeem_coordinates}")
else:
    print("Auto redeem mode is disabled.")

# ... (rest of your existing code)

def display_message(channelid, message):
    message_id = message.get('id')
    if message_id not in retrieved_message_ids:
        retrieved_message_ids.add(message_id)
        author_id = message.get('author', {}).get('id')
        content = message.get('content')
        if author_id in target_user_ids and content not in user_messages:
            cleaned_content = remove_discord_formatting(content)
            if cleaned_content.strip():  # Check if the cleaned content is not empty
                print(colorama.Fore.YELLOW + "Message:")
                print(cleaned_content)
                print(colorama.Style.RESET_ALL)

                copy_to_clipboard(cleaned_content)  # Copy the cleaned message content to the clipboard
                user_messages.add(content)
                play_sound("t.mp3")  # Play the sound "t.mp3"

                if auto_enter_mode:
                    perform_auto_enter()  # Perform auto enter if enabled

                if auto_click_mode and auto_redeem_coordinates:
                    # Automatically click redeem at the specified coordinates
                    pyautogui.click(auto_redeem_coordinates[0], auto_redeem_coordinates[1])
                    print(colorama.Fore.GREEN + "*Clicked Redeem*")
                    print(colorama.Style.RESET_ALL)

def remove_discord_formatting(content):
    # Remove '# ' from the beginning
    content = re.sub(r'^#\s*', '', content)
    
    # Handle triple backticks (``` ... ```)
    code_blocks = re.findall(r'```.*?```', content, flags=re.DOTALL)
    for block in code_blocks:
        content = content.replace(block, block[3:-3])  # Remove triple backticks

    # Remove double backticks
    content = re.sub(r'`.*?`', '', content)
    
    # Remove strikethrough
    content = re.sub(r'~~(.*?)~~', r'\1', content)
    
    return content

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

# Perform auto enter (Ctrl + V, Enter)
def perform_auto_enter():
    try:
        clipboard.paste()  # Paste the clipboard content
        keyboard.press_and_release('enter')  # Simulate Enter key press
    except Exception as e:
        print("Error performing auto enter:", e)

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

    time.sleep(0.2)  # Add a wait time of 0.2 seconds before the next iteration
