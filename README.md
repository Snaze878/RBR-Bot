# RBR Discord Bot

Welcome to the **RBR Discord Bot**!  
This bot scrapes online leaderboards from [rallysimfans.hu](https://rallysimfans.hu/) and posts real-time updates to Discord. Whether you're tracking your rally team's progress or keeping tabs on the competition, this bot has you covered.

Note - I also have a way smarter and more polished version of this bot here, but it also requires a database: https://github.com/Snaze878/RBR_Bot_MySQL

---

## 🏎️ Features

- **Automated Leaderboard Updates**  
  Continuously scrapes and posts the latest rally standings to your Discord server.

- **Live Leader Change Detection**  
  Announces when a new driver takes the lead in any rally leg.

- **Custom Chat Commands**  
  Use commands to retrieve top performers, rally info, and CSV-based point standings.

- **Multi-Leg Event Support**  
  Handles tracking and announcements across six rally legs with three stages each.

- **Archived Leaderboards**  
  View past week results with dedicated commands.

- **CSV Standings Parsing**  
  Reads `standings.csv` to display custom season-long driver points.

---

## 💬 Commands

```
!leaderboard       → Shows the general leaderboard (top 10).
!leg1 to !leg6     → Displays top 5 results for each track in the specified rally leg.
!info              → Shows competition name, password, and rally URL.
!points            → Displays season-long standings from standings.csv.
!s1w1              → Shows archived results from Season 1, Week 1.
```

---

## ⚙️ How It Works

The bot uses `requests` and `BeautifulSoup` to scrape HTML tables from RallySimFans and parses the results. It detects leader changes in real time and posts rich embedded messages in Discord using `discord.py`. It also loads URLs and bot tokens from a secure `.env` file and supports dynamic commands for accessing results.

---

## 📜 License

This project is open-source and licensed under the **GNU General Public License v3**.  
Feel free to modify and distribute it under the terms of the license.

---

## 🤝 Contribute & Get Support

Want to contribute or report a bug? Pull requests and issue reports are welcome!  
Join the support community here:

**[🌐 Discord Support Server](https://discord.gg/HbRaM2taQG)**

---

# 🛠️ Installation Guide

## 1. Install Python

Download Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
✅ Be sure to check **“Add Python to PATH”** during installation.

---

## 2. Install Required Packages

Run the following in your terminal:

```bash
pip install discord.py requests beautifulsoup4
pip install python-dotenv selenium webdriver-manager
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
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
LEADERBOARD_URL=https://example.com/leaderboard
S1W1_URL=https://example.com/season1week1
INFO_URL=https://example.com/info
RALLY_NAME=My Rally Event
RALLY_PASSWORD=examplepass
LEG_1_1=https://example.com/leg1/track1
LEG_1_2=https://example.com/leg1/track2
LEG_1_3=https://example.com/leg1/track3
...
LEG_6_3=https://example.com/leg6/track3
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
