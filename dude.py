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

# Function to save auto action coordinates to a file
def save_auto_action_coordinates(x, y, filename):
    with open(filename, "w") as f:
        f.write(f"{x},{y}")

# Function to load auto action coordinates from a file
def load_auto_action_coordinates(filename):
    try:
        with open(filename, "r") as f:
            coordinates = f.read().strip().split(',')
            if len(coordinates) == 2:
                return int(coordinates[0]), int(coordinates[1])
    except (FileNotFoundError, ValueError):
        pass
    return None

# Function to get confirmation for coordinates
def get_coordinates_confirmation(filename, action_name):
    use_existing = input(f"Would you like to use the last {action_name} coordinates? (y/n): ")
    if use_existing.lower() == 'y':
        existing_coordinates = load_auto_action_coordinates(filename)
        if existing_coordinates:
            print(f"Using existing {action_name} coordinates: {existing_coordinates}")
            return existing_coordinates
    print(f"Please hover your mouse over the {action_name} and press 's' to save the coordinates.")
    keyboard.wait('s', suppress=True)
    new_coordinates = pyautogui.position()
    save_auto_action_coordinates(new_coordinates[0], new_coordinates[1], filename)
    print(f"New {action_name} coordinates saved: {new_coordinates}")
    return new_coordinates

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
        auto_action_mode = settings_data.get("auto_action_mode", False)
        textbox_coordinates_file_name = settings_data.get("textbox_coordinates_file_name", "textbox_coordinates.txt")
        redeem_coordinates_file_name = settings_data.get("redeem_coordinates_file_name", "redeem_coordinates.txt")
except (FileNotFoundError, json.JSONDecodeError):
    bot_token = ""
    target_user_ids = []
    target_channels = []
    auto_action_mode = False
    textbox_coordinates_file_name = "textbox_coordinates.txt"
    redeem_coordinates_file_name = "redeem_coordinates.txt"

# Check if auto action mode is enabled
textbox_coordinates = None
redeem_coordinates = None

if auto_action_mode:
    textbox_coordinates = get_coordinates_confirmation(textbox_coordinates_file_name, "textbox")
    redeem_coordinates = get_coordinates_confirmation(redeem_coordinates_file_name, "redeem button")

else:
    print("Auto action mode is disabled.")

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

                if auto_action_mode:
                    # Click the textbox
                    pyautogui.click(textbox_coordinates[0], textbox_coordinates[1])
                    # Paste the clipboard content
                    perform_auto_enter()
                    
                    # Click the redeem button
                    pyautogui.click(redeem_coordinates[0], redeem_coordinates[1])
                    
                    # Click the textbox again
                    pyautogui.click(textbox_coordinates[0], textbox_coordinates[1])

                    print(colorama.Fore.GREEN + "Auto redeem done")
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
        keyboard.press_and_release('ctrl+v')  # Simulate Ctrl + V
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
