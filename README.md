About RBR Discord Bot
-----
Welcome to the RBR Discord Bot! This bot is designed to scrape online leaderboards and provide real-time updates on rally standings from https://rallysimfans.hu/. Whether you're part of a rally group looking to keep track of everyone's performance or just want to stay updated on the competition, this bot ensures you never miss a leaderboard update.

------

Features:

Automated Leaderboard Updates: The bot scrapes the rally leaderboard and posts updates in Discord.

Real-Time Leader Changes: Notifies the server when there is a new leader in a rally leg.

Custom Commands: Retrieve top performers and detailed rally standings using simple commands.

Dynamic Event Tracking: Supports multiple rally legs, ensuring full coverage of the competition.

Info Retrieval: Provides important rally details like championship name and password.

------

Commands:

!top5 - Displays the top 5 competitors from each rally leg.

!leaderboard - Fetches the general leaderboard.

!leg1, !leg2, ..., !leg6 - Displays the top 5 standings for a specific rally leg.

!info - Retrieves essential rally details like competition name and access credentials.

------

How It Works:

The bot uses web scraping to extract leaderboard data from your rallysimfans group. It processes the information and presents it in an easy-to-read format on Discord. By continuously monitoring changes, the bot ensures that users receive timely updates on race progress.

------

Open-Source & Licensing:

The RBR Discord Bot is open-source software, released under the GNU General Public License v3. This means you are free to modify and distribute it as long as you comply with the license terms.

------

Contributions & Support:

If you'd like to contribute to the project or report issues, feel free to get involved! The bot is continuously improving, and community feedback is always welcome.

Enjoy the races and stay updated with RBR Discord Bot!






RBR Discord Bot Installation Guide

------

Install:
----
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

Go to Discord Developer Applications Website: https://discord.com/developers/applications

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
