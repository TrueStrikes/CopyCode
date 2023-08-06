# CopyCat 2.0 Discord Bot

The CopyCat Discord Bot is a Python script that monitors specified Discord channels for messages sent by specific users. When it detects a message from the target user, it copies the message content to the clipboard and plays a sound.

## Instructions

1. **Requirements:**

   - Python 3.6 or later
   - External modules: `requests`, `pygame`, `colorama`, `clipboard`

2. **Installation:**

   - Clone this repository to your local machine or download the script.

3. **Setting up the Configuration:**

   - Create a new `config.json` file in the same directory as the script.
   - Fill in the `config.json` with the following content:

     ```json
     {
         "config_filename": "settings.json"
     }
     ```

   - Create a new file named `settings.json` in the same directory as the script and fill it with the appropriate information:

     ```json
     {
         "bot_token": "YOUR_USER_TOKEN",
         "target_user_ids": ["TARGET_USER_ID_1", "TARGET_USER_ID_2"],
         "target_channels": ["TARGET_CHANNEL_ID_1", "TARGET_CHANNEL_ID_2"]
     }
     ```

     Replace `"YOUR_BOT_TOKEN"`, `"TARGET_USER_ID_1"`, `"TARGET_USER_ID_2"`, `"TARGET_CHANNEL_ID_1"`, and `"TARGET_CHANNEL_ID_2"` with the actual values from your Discord bot token and target user/channel IDs.

4. **Running the Script:**

   - Open a terminal or command prompt and navigate to the directory where the script is located.
   - Run the script using the command: `python dude.py`.

5. **Usage:**

   - The script will start monitoring the specified Discord channels for messages from the target users.
   - When it detects a message from a target user, it will copy the message content to the clipboard and play the sound "t.mp3" to alert you.

6. **Stopping the Script:**

   - To stop the script, press `Ctrl + C` in the terminal where the script is running.

## Notes

- The script uses the `requests` module to interact with the Discord API, so make sure your bot token has the necessary permissions to read messages in the specified channels.
- Ensure that the `pygame` module is installed for the sound to work. You can install it using `pip install pygame`.
- The script will automatically ignore duplicate messages from the same user and avoid copying them to the clipboard multiple times.
- Messages starting with `# ` will be copied without the `# ` prefix.

## Possible Errors and Fixes

1. **`NameError: name 'bot_token' is not defined`:**

   If you encounter this error, it means that the `bot_token` variable is not set. Double-check the `settings.json` file and ensure that the `"bot_token"` field contains your Discord bot token.

2. **`KeyError: 'target_user_ids'`:**

   This error occurs when the `"target_user_ids"` field is missing or empty in the `settings.json` file. Ensure that you have specified at least one target user ID in the `"target_user_ids"` list.

3. **`KeyError: 'target_channels'`:**

   Similar to the previous error, this one happens when the `"target_channels"` field is missing or empty in the `settings.json` file. Ensure that you have specified at least one target channel ID in the `"target_channels"` list.

4. **Sound Not Playing:**

   If the sound "t.mp3" is not playing, make sure that the file exists in the same directory as the script and that the `pygame` module is installed correctly.

5. **Messages Not Being Detected:**

   If the script is not detecting messages, verify that the bot token has the necessary permissions to access the specified channels and read messages.

If you encounter any other issues or have any further questions, feel free to reach out, and I'll be happy to assist you further.

## Disclaimer

This script is provided as-is, and the use of this script to interact with Discord should comply with the Discord Terms of Service and Guidelines. Use it responsibly and avoid violating Discord's rules or any applicable laws.

Feel free to modify and improve the script as needed.
