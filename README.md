Here's a cleaner, more polished version of your `README.md` that's structured for clarity and professional presentation on GitHub:

---

# RBR Discord Bot

Welcome to the **RBR Discord Bot**!  
This bot is designed to scrape online leaderboards and provide real-time updates from [rallysimfans.hu](https://rallysimfans.hu/). Whether you're tracking your rally team's progress or just want to stay up to date with the competition, this bot ensures you never miss a moment.

---

## 🚗 Features

- **Automated Leaderboard Updates**  
  Scrapes the rally leaderboard and posts updates directly to Discord.

- **Real-Time Leader Changes**  
  Notifies the server when there's a new leader in a rally leg.

- **Custom Commands**  
  Retrieve top performers and detailed standings using simple chat commands.

- **Dynamic Event Tracking**  
  Supports multiple rally legs for full event coverage.

- **Info Retrieval**  
  Displays key rally details like championship name and password.

---

## 💬 Commands

```
!leaderboard     → Shows the general leaderboard.
!leg1 to !leg6   → Displays top 5 results for the specified rally leg.
!info            → Shows competition name and access credentials.
```

---

## ⚙️ How It Works

The bot scrapes leaderboard data from your RallySimFans group, processes the information, and posts updates in a readable format on Discord. It continuously monitors for changes to provide timely alerts on race progress.

---

## 🧾 License

This project is open-source and licensed under the **GNU General Public License v3**.  
Feel free to modify and distribute it under the terms of the license.

---

## 🤝 Contribute & Get Support

Want to contribute or report a bug? Pull requests and issue reports are welcome!  
Join the support community here:

**[🌐 Discord Support Server](https://discord.gg/HbRaM2taQG)**

---

# 🛠 Installation Guide

## 1. Install Python

Download Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
✅ Be sure to check **“Add Python to PATH”** during installation.

---

## 2. Install Required Packages

Run the following in your terminal:

```bash
pip install discord.py requests beautifulsoup4
pip install python-dotenv selenium
```

---

## 3. Create Your Discord Bot

- Visit: [Discord Developer Portal](https://discord.com/developers/applications)
- Click **“New Application”**, name it, and go to the **Bot** tab.
- Click **“Add Bot”** and enable **Message Content Intent**.

---

## 4. Set Bot Permissions

Ensure the bot has the following permissions:

- Send Messages  
- Embed Links  
- Read Message History  
- Use External Emojis  

---

## 5. Generate OAuth2 URL

- In the **OAuth2** tab, use the URL Generator:
  - Select `bot` scope
  - Assign the permissions listed above
- Set integration type to **Guild Install**  
- Copy and paste the generated URL into your browser to invite the bot to your server.

---

## 6. Download the Bot Files

Place `RBR_Bot.py` and `.env` in a directory like:

```
C:\Users\YOUR_NAME\
```

> ⚠️ Rename `.env.txt` to just `.env` if necessary.

---

## 7. Configure the .env File

Open `.env` and add your details:

```env
DISCORD_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
RALLY_URL=https://example.com
RALLY_NAME=My Rally Event
RALLY_PASSWORD=examplepass
LEADERBOARD_URL=https://example.com/leaderboard
LEG1_URL=https://example.com/leg1
LEG2_URL=https://example.com/leg2
...
```

> 🔐 **Never share your bot token publicly.**

---

## 8. Enable Developer Mode in Discord

- Go to **User Settings > Advanced > Developer Mode**.
- Right-click a channel → **Copy Channel ID** and paste into your `.env`.

---

## 9. Run the Bot

Open a terminal, navigate to the bot's folder:

```bash
cd path\to\your\bot
python RBR_Bot.py
```

You're all set! 🎉 The bot should now be running and posting updates in your selected channel.

