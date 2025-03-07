RBR-Bot

RBR Discord Bot Installation Guide

------

Install:

1. Install Python:

Download Python from the official website. https://www.python.org/downloads/

During installation, make sure to "Add Python.exe to PATH" on the first screen.

------

2. Install Required Python Packages:

Run the following commands in a terminal:

pip install discord.py requests beautifulsoup4
pip install python-dotenv
pip install selenium

------

3. Create a Discord Bot:

Go to Discord Developer Applications

Click New Application, name your bot, and build it.

Navigate to Bot on the left menu.

Enable Message Content Intent.

------

4. Set Bot Permissions:

The bot should have the following permissions:

Send messages

Embed links

Read message history

Use external emojis

------

5. Generate an OAuth2 URL:

Go to the OAuth2 tab.

Under OAuth2 URL Generator, select bot.

The Bot Permissions section will appear—ensure the bot has the correct permissions as listed above.

Set Integration Type to Guild Install.

Copy the generated URL and paste it into your browser.

Select the Discord server where you want to add the bot.

------

6. Download the Bot Files:

Download RBR_Bot.py and the .env file.

Place them under your user directory, e.g., C:\Users\YOUR_NAME.

------

7. Configure the .env File:

Open the .env file in a text editor.

Add your Discord Bot Token (found under Bot in the Discord Developer portal). DO NOT SHARE THIS TOKEN!

------

8. Set Up the Channel ID:

In Discord, go to Settings > App Settings > Advanced and enable Developer Mode.

Go to your Discord server, right-click the desired text channel, and select Copy Channel ID.

Paste this into DISCORD_CHANNEL_ID in your .env file.

------

9. Configure Rally Team Details:

Add your Rally URL, Rally Name, and Password.

Add the Leaderboard URL and any other leg URLs as needed.

Example values are provided in the .env file.

------

10. Run the Bot:

Open CMD (Command Prompt).

Navigate to the directory where RBR_Bot.py is stored.

Run the bot with: 
  python RBR_Bot.py
