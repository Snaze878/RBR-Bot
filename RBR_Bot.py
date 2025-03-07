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
            name_parts = name_vehicle.split(" / ", 1)
            if len(name_parts) > 1:
                name1 = name_parts[0].strip()  # "Name Before the /"
                name2_vehicle = name_parts[1].strip()  # "Name after the /"
                # Now, separate the name from the vehicle
                for vehicle_start in ["Citroen", "Ford", "Peugeot", "Opel"]:  # Extend this list if needed
                    if vehicle_start in name2_vehicle:
                        name2 = name2_vehicle.split(vehicle_start, 1)[0].strip()  # "Name"
                        vehicle = vehicle_start + name2_vehicle.split(vehicle_start, 1)[1].strip()  # "Vehicle"
                        break
                else:
                    # If no vehicle is found in the second part, treat the entire second part as name
                    name2 = name2_vehicle
                    vehicle = ""
            else:
                name1 = name_parts[0].strip()
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
    "Leg 1": os.getenv("LEG_1_URL"),
    "Leg 2": os.getenv("LEG_2_URL"),
    "Leg 3": os.getenv("LEG_3_URL"),
    "Leg 4": os.getenv("LEG_4_URL"),
    "Leg 5": os.getenv("LEG_5_URL"),
    "Leg 6": os.getenv("LEG_6_URL")
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
        for leg_name, url in URLS.items():
            leaderboard = scrape_leaderboard(url)
            if leaderboard:
                current_leader = leaderboard[0]["name"]
                if url in previous_leaders:
                    previous_leader = previous_leaders[url]
                    # Only send a message if the leader has changed
                    if previous_leader != current_leader:
                        await channel.send(f"New leader for {leg_name}: {current_leader} (previously {previous_leader})! URL {url}")

                
                # Update the previous leader to the current leader
                previous_leaders[url] = current_leader
        
        await asyncio.sleep(60)  # Adjust wait time if needed to refresh

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.loop.create_task(check_leader_change())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Handle !top5 command
    if message.content.startswith("!top5"):
        for leg_name, url in URLS.items():
            leaderboard = scrape_leaderboard(url)
            if leaderboard:
                print(f"Top 5 extracted from {leg_name}: {leaderboard[:5]}")
                top5 = "\n".join([f"**{entry['position']}**. **{entry['name']}** :race_car: {entry['vehicle']} :hourglass: ({entry['diff_first']})" for entry in leaderboard[:5]])
                await message.channel.send(f"-----------------\n\n**Top 5 Leaderboard for {leg_name}:**\n{top5}\n\n")
            else:
                await message.channel.send(f"Couldn't retrieve leaderboard for {leg_name}.")
    
    # Handle !leg1, !leg2, etc. dynamically
    elif message.content.startswith("!leg"):
        leg_number = message.content[4:]
        if leg_number in ['1', '2', '3', '4', '5', '6']:
            url = URLS[f"Leg {leg_number}"]
            leaderboard = scrape_leaderboard(url, table_class="rally_results_stres_left")
            if leaderboard:
                top5 = "\n".join([f"**{entry['position']}**. **{entry['name']}** :race_car: {entry['vehicle']} :hourglass: ({entry['diff_first']})" for entry in leaderboard[:5]])
                await message.channel.send(f"**Top 5 for Leg {leg_number}:**\n{top5}")
            else:
                await message.channel.send(f"Couldn't retrieve leaderboard for Leg {leg_number}.")
    
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
