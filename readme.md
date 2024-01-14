# CopyCat Discord Bot

The CopyCat Discord Bot is a Python script designed to efficiently monitor specified Discord channels for user-generated content (UGC) codes. It is intended to automate the process of sniping UGC codes, which can often be time-sensitive due to their limited availability.


**Tydummy.py only works with stealing from typedummy bot**

## Purpose

Many online communities frequently share UGC codes (e.g., game item codes, discounts, giveaways) within Discord channels. CopyCat provides a way to swiftly capture and utilize these codes using a bot, enhancing your chances of obtaining them before they expire.

## Instructions

### Requirements:

- Python 3.6 or later
- External modules: `requests`, `pygame`, `colorama`, `clipboard`

### Installation:

1. Clone this repository to your local machine or download the script.

2. Open a terminal or command prompt and navigate to the directory where the script is located.

3. Install the required external modules using the following command:


### Usage:

1. **Configuring the Bot:**

- Create a new `config.json` file in the same directory as the script.
- Fill in the `config.json` with the following content:

  ```json
  {
      "config_filename": "settings.json"
  }
  ```

- Create a new file named `settings.json` in the same directory as the script (`dude.py`) and configure it with your Discord bot token, target user IDs, and target channel IDs. For example:

  ```json
  {
      "bot_token": "YOUR_USER_TOKEN",
      "target_user_ids": ["TARGET_USER_ID_1", "TARGET_USER_ID_2"],
      "target_channels": ["TARGET_CHANNEL_ID_1", "TARGET_CHANNEL_ID_2"]
  }
  ```

  Replace `"YOUR_USER_TOKEN"`, `"TARGET_USER_ID_1"`, `"TARGET_USER_ID_2"`, `"TARGET_CHANNEL_ID_1"`, and `"TARGET_CHANNEL_ID_2"` with your actual values.

- To find your Discord user token, you can watch this tutorial video: [How to Get a Discord user Token](https://www.youtube.com/watch?v=YjiQ7CajAgg)
- To find the channel ID, you can watch this tutorial video: [How to Get a Discord Channel ID](https://www.youtube.com/watch?v=YEgFvgg7ZPI)

2. **Running the Script:**

- In the terminal or command prompt, navigate to the directory where the script (`dude.py`) is located.

- Install the required external modules using the following command:

  ```
  pip install requests pygame colorama clipboard
  ```

- Run the script using the following command:

  ```
  python dude.py
  ```

- The script will start monitoring the specified Discord channels for messages from the target users.
- When it detects a message from a target user, it will copy the message content to the clipboard and play the sound "t.mp3" to alert you.

### Creating Multiple "Preloads":

You can set up multiple configurations ("preloads") by creating additional JSON files based on the template provided. Each JSON file can contain a different combination of bot token, target user IDs, and target channel IDs. This allows you to quickly switch between different settings without modifying the main script.

Follow these steps to create and use multiple "preloads":

1. **Create a New JSON File:**

- Duplicate the `settings.json` file and rename it to something meaningful (e.g., `preload1.json`, `preload2.json`, etc.).

2. **Edit the New JSON File:**

- Open the new JSON file using a text editor.
- Modify the `bot_token`, `target_user_ids`, and `target_channels` values to your desired settings.

  ```json
  {
      "bot_token": "NEW_USER_TOKEN",
      "target_user_ids": ["NEW_TARGET_USER_ID_1", "NEW_TARGET_USER_ID_2"],
      "target_channels": ["NEW_TARGET_CHANNEL_ID_1", "NEW_TARGET_CHANNEL_ID_2"]
  }
  ```

3. **Update `config.json`:**

- Open the `config.json` file and replace the `config_filename` value with the filename of your new JSON file.

  ```json
  {
      "config_filename": "preload1.json"
  }
  ```

- Now the script will load the settings from the new JSON file specified in `config.json`.

4. **Run the Script:**

- Follow the previous instructions to install external modules and run the script using the new JSON file.

Using this method, you can easily switch between different "preloads" by changing the `config.json` file. Each JSON file represents a unique configuration that you can quickly switch to without modifying the main script.

**Quick note**
- Auto action mode automatically click the redeem button and the textbot for you, so you can be "safe" if you have slow reflexes.

### Important Notes:

- Be sure to name your new JSON files meaningfully to reflect the different configurations you're using.
- Always ensure that the JSON syntax is correct in your new configuration files to avoid errors.
- The script will only load settings from the JSON file specified in `config.json`.

Feel free to customize and organize your configurations based on your needs.

### Disclaimer


# For support join https://discord.gg/uWsd5Bp4 and create a ticket
