import asyncio
import datetime
import os
from itertools import cycle

import aiohttp
import discord
import tasks
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands, tasks

from config import TOKEN


class MyBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix ='!',
            intents=discord.Intents.all(),
            application_id = 1242377989048762418)

        self.initial_extensions = [
            "cogs.admin.timeout",
            "cogs.welcome.introduce",
            "cogs.welcome.hello",
            "cogs.welcome.say",
            "cogs.welcome.who_are_you",
            #"cogs.Spotify.spotify",
            "cogs.games.yahtzee",
            #"cogs.economy.pay",
            #"cogs.gamble.slot"
]

    async def setup_hook(self):   
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync()

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")
        name_change.start()
        print(launch_time)
        bot.loop.create_task(name_change())

bot = MyBot()

launch_time = datetime.datetime.now(datetime.timezone.utc)

@tasks.loop(seconds=1, count=None, reconnect=True)
async def name_change():
    delta_uptime = datetime.datetime.now(datetime.timezone.utc) - launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    print(f"Online Time: {days:02d}d | {hours:02d}h | {minutes:02d}m | {seconds:02d}s")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            large_image = "https://random.jpg",
            large_text = "This is Game Icon",
            name = "Board Games",
            details = "Yahtzee Duel",
            state = f"{days:02d}d | {hours:02d}h | {minutes:02d}m Passed"
        )
    )

    #await asyncio.sleep(5400)
    #await bot.change_presence(
        #status=discord.Status.online,
        #activity=discord.Activity(
            #type=discord.ActivityType.listening, 
            #large_image = "",
            #large_text = "This is Game Icon",
            #name = "Spotify",
            #details = "House Mix",
            #state = f"{days:02d}d | {hours:02d}h | {minutes:02d}m Passed"

        #)
    #)

#bot = commands.Bot(command_prefix="!" , intents=discord.Intents.all())

#@bot.event
#async def on_ready():
    #print("Bot is Up and Ready!")
    #print(launch_time)
    #name_change.start()
    #bot.loop.create_task(name_change())
    #try:
        #synced = await bot.tree.sync()
        #print(f"Synced {len(synced)} command(s)")
    #except Exception as e:
        #print(e)

# bot_status = cycle(["Secret Things...","cooking"])

#@bot.tree.command(name="hello")
#async def hello(
    #interaction: discord.Interaction):
    #await interaction.response.send_message(
        #f"Hey {interaction.user.mention}! This is a slash command!", ephemeral = True)

#@bot.tree.command(name="who_are_you")
#async def who_are_you(
    #interaction: discord.Interaction):
    #await interaction.response.send_message(
        #f"Hey {interaction.user.mention}! I am a discord bot developed by the user 'Jasonkami.'!")

#@bot.tree.command(name="say")    
#@app_commands.describe(
    #thing_to_say = "What should I say?")
#async def say(
    #interaction: discord.Interaction, 
    #thing_to_say: str):
    #await interaction.response.send_message(
        #f"{interaction.user.name} said: `{thing_to_say}`")

#@bot.tree.command(name = "introduce", description = "Introduce yourself to the server!")

#@app_commands.describe(
    #name = "Your name",
    #age = "Your age")

#@app_commands.choices(age = [
    #Choice(name = "one", value = 1),
    #Choice(name = "two", value = 2),
    #Choice(name = "three", value = 3),
    #Choice(name = "older than three", value = 4)
#])

#async def introduce(
    #interaction: discord.Interaction,
    #name: str,
    #age: int) -> None:
    #await interaction.response.send_message(
        #f"My name is {name} and I am {age} years old!")

#@bot.tree.command(name="lolol")
#async def lolol(
    #interaction: discord.Interaction):
    #await interaction.response.send_message(
        #f"lolol")

async def dontcrash():
    channels = bot.get_all_channels()
    await asyncio.sleep(45)
    print("Channels have been refreshed!")

bot = MyBot()
bot.run(TOKEN)