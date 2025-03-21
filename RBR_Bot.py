# My RBR Discord Bot - Scrapes a website and outputs leaderboards
# Copyright (C) 2025 Snaze878
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


import discord
import asyncio
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
LEADERBOARD_URL = os.getenv("LEADERBOARD_URL") #Update Leaderboard in the .env file.


# Function to scrape the general leaderboard
def scrape_general_leaderboard(url, table_class="rally_results"):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Unable to fetch the page for {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    leaderboard = []
    tables = soup.find_all("table", {"class": table_class})  

    if not tables:
        print(f"Table not found for {url}!")
        return []
    
    table = tables[1]  # Select the first table found (adjusted if needed)
    table_rows = table.find_all("tr")
    
    print(f"Found {len(table_rows)} rows for {url}")
    
    for index, row in enumerate(table_rows[0:]):  # Skip header row if needed
        columns = row.find_all("td")
        if len(columns) >= 7:
            position = columns[0].text.strip()
            name = columns[1].text.strip()
            makelogo = columns[2].text.strip()
            vehicle = columns[3].text.strip()
            time = columns[4].text.strip()
            diff_prev = columns[5].text.strip()
            diff_first = columns[6].text.strip()
            sr = columns[7].text.strip()
            
           
            entry = {
                "position": position,
                "name": name,
                "vehicle": vehicle,
                "diff_prev": diff_prev,
                "diff_first": diff_first
            }
            leaderboard.append(entry)
            print(f"Row {index + 1} - Added: {entry} from {url}")

    print(f"Final leaderboard ({len(leaderboard)} entries) for {url}: {leaderboard}")
    return leaderboard

# Function to scrape the leaderboard for each leg
def scrape_leaderboard(url, table_class="rally_results_stres_right"):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Unable to fetch the page for {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    leaderboard = []
    tables = soup.find_all("table", {"class": table_class})  

    if not tables:
        print(f"Table not found for {url}!")
        return []
    
    table = tables[1]  # Select the first table found
    table_rows = table.find_all("tr")
    
    print(f"Found {len(table_rows)} rows for {url}")
    
    for index, row in enumerate(table_rows[0:]):  # Skip header row if needed
        columns = row.find_all("td")
        if len(columns) >= 5:
            position = columns[0].text.strip()
            name_vehicle = columns[1].text.strip()
            time = columns[2].text.strip()
            diff_prev = columns[3].text.strip()
            diff_first = columns[4].text.strip()
            
            # Split the name and vehicle into 3 parts. Have to do this due to how the website table is setup. 
            # Split the name and vehicle into parts
            name_parts = name_vehicle.split(" / ", 1)

            vehicle_starts = [
                "Citroen", "Ford", "Peugeot", "Opel", "Abarth", "Skoda", "Mitsubishi", "Subaru", "BMW", "GM", "GMC",
                "Toyota", "Honda", "Suzuki", "Acura", "Audi", "Volkswagen", "Chevrolet", "Volvo", "Kia", "Jeep", "Dodge",
                "Mazda", "Hyundai", "Buick", "MINI", "Porsche", "Mercedes", "Land Rover", "Alfa Romeo", "Lancia"
            ]

            if len(name_parts) > 1:
                name1 = name_parts[0].strip()
                name2_vehicle = name_parts[1].strip()
                for brand in vehicle_starts:
                    if brand in name2_vehicle:
                        name2 = name2_vehicle.split(brand, 1)[0].strip()
                        vehicle = brand + " " + name2_vehicle.split(brand, 1)[1].strip()
                        break
                else:
                    name2 = name2_vehicle
                    vehicle = ""
            else:
                combined = name_parts[0].strip()
                for brand in vehicle_starts:
                    if brand in combined:
                        name1 = combined.split(brand, 1)[0].strip()
                        vehicle = brand + " " + combined.split(brand, 1)[1].strip()
                        name2 = ""
                        break
                else:
                    name1 = combined
                    name2 = ""
                    vehicle = ""


            full_name = f"{name1} / {name2}"  # Combine both name parts
            entry = {
                "position": position,
                "name": full_name,
                "vehicle": vehicle,
                "diff_prev": diff_prev,
                "diff_first": diff_first
            }
            leaderboard.append(entry)
            print(f"Row {index + 1} - Added: {entry} from {url}")

    print(f"Final leaderboard ({len(leaderboard)} entries) for {url}: {leaderboard}")
    return leaderboard

# Bot setup

TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Discord bot token. Put it into the .env file.

# Urls will all go into the .env file.
URLS = {
    "Leg 1": [os.getenv("LEG_1_1"), os.getenv("LEG_1_2"), os.getenv("LEG_1_3")],
    "Leg 2": [os.getenv("LEG_2_1"), os.getenv("LEG_2_2"), os.getenv("LEG_2_3")],
    "Leg 3": [os.getenv("LEG_3_1"), os.getenv("LEG_3_2"), os.getenv("LEG_3_3")],
    "Leg 4": [os.getenv("LEG_4_1"), os.getenv("LEG_4_2"), os.getenv("LEG_4_3")],
    "Leg 5": [os.getenv("LEG_5_1"), os.getenv("LEG_5_2"), os.getenv("LEG_5_3")],
    "Leg 6": [os.getenv("LEG_6_1"), os.getenv("LEG_6_2"), os.getenv("LEG_6_3")]
}

CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID") ) # Discord channel ID. Put it into the .env file.

intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)  

previous_leaders = {}

async def check_leader_change():
    global previous_leaders
    await bot.wait_until_ready()

    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Error: Discord channel not found!")
        return

    while not bot.is_closed():
        try:
            for leg_name, urls in URLS.items():
                for idx, url in enumerate(urls):
                    if not url:
                        continue

                    leaderboard = scrape_leaderboard(url)
                    if leaderboard:
                        current_leader = leaderboard[0]["name"]
                        current_time = leaderboard[0]["diff_first"]
                        track_name = f"{leg_name} - Track {idx + 1}"

                        previous = previous_leaders.get(track_name)

                        if previous and previous.get("name") != current_leader:
                            previous_name = previous.get("name", "Unknown")
                            previous_time = previous.get("time", "N/A")

                            embed = discord.Embed(
                                title="🏆 New Track Leader!",
                                description=(
                                    f"**{current_leader}** is now leading **{track_name}**\n"
                                    f"(Previously: {previous_name})\n"
                                    f"**Time Diff:** `{previous_time} → {current_time}`"
                                ),
                                color=discord.Color.gold()
                            )
                            await channel.send(embed=embed)

                        previous_leaders[track_name] = {
                            "name": current_leader,
                            "time": current_time
                        }

            await asyncio.sleep(60)

        except Exception as e:
            print(f"[ERROR] Exception in check_leader_change: {e}")
            await asyncio.sleep(60)  # Sleep anyway to avoid tight error loop


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.loop.create_task(check_leader_change())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    
    # Handle !leg command dynamically
    if message.content.startswith("!leg"):
        leg_number = message.content[4:].strip()  # Extract leg number from the command

        if leg_number not in ['1', '2', '3', '4', '5', '6']:
            await message.channel.send("Invalid leg number! Please use `!leg1`, `!leg2`, etc.")
            return

        # Get available URLs for this leg, filtering out None values
        leg_urls = [url for url in URLS.get(f"Leg {leg_number}", []) if url]

        if not leg_urls:
            await message.channel.send(f"⚠️ No leaderboard data available for Leg {leg_number}.")
            return

        # Scrape and format leaderboards dynamically
        def scrape_and_format(url, source):
            leaderboard = scrape_leaderboard(url, table_class="rally_results_stres_right")  # Adjust table class if needed
            if not leaderboard:
                return f"❌ No leaderboard data available from {source}."
            
            top_entries = leaderboard[:5]  # Get only the top 5
            formatted_results = "\n".join(
                [f"**{entry['position']}**. **{entry['name']}** 🏎️ {entry['vehicle']} ⏳ ({entry['diff_first']})"
                 for entry in top_entries]
            )
            return f"🏁 **Top 5 for {source}:**\n{formatted_results}"

        # Prepare the output
        leaderboard_messages = []
        for idx, url in enumerate(leg_urls, start=1):
            result = scrape_and_format(url, f"Leg {leg_number} (Track {idx})")
            if result:
                leaderboard_messages.append(result)

        # Combine all results with separators
        response = "\n\n────────────────────\n\n".join(leaderboard_messages) if leaderboard_messages else f"⚠️ No data available for Leg {leg_number}."
        
        await message.channel.send(response)


    
    # Handle !leaderboard command
    elif message.content.startswith("!leaderboard"):
        leaderboard = scrape_general_leaderboard(LEADERBOARD_URL)
        if leaderboard:
            top5 = "\n".join([f"**{entry['position']}**. **{entry['name']}** :race_car: {entry['vehicle']} :hourglass: ({entry['diff_first']})" for entry in leaderboard[:10]])
            await message.channel.send(f"**General Leaderboard:**\n{top5}")
        else:
            await message.channel.send("Couldn't retrieve the general leaderboard.")


    # Load additional environment variables for !info command
    INFO_URL = os.getenv("INFO_URL")
    RALLY_NAME = os.getenv("RALLY_NAME")
    RALLY_PASSWORD = os.getenv("RALLY_PASSWORD")

    # Handle !info command
    if message.content.startswith("!info"):
        if INFO_URL and RALLY_NAME and RALLY_PASSWORD:
            await message.channel.send(
                f"**Here is the link:** {INFO_URL}\n"
                f"**Rally Championship Name:** {RALLY_NAME}\n"
                f"**Password:** {RALLY_PASSWORD}"
            )
        else:
            await message.channel.send("Error: Some information is missing in the `.env` file.")

    # Ensure bot continues processing other commands
    await bot.process_commands(message)

bot.run(TOKEN)
