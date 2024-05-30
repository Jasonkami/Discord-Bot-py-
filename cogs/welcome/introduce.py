import discord
from discord import app_commands
from discord.app_commands import Choice, Command
from discord.ext import commands


class introduce(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(
    name = "introduce",
    description = "Introduce Yourself!")

  @app_commands.describe(
    name = "Your name",
    age = "Your age")

  @app_commands.choices(age = [
  Choice(name = "one", value = 1),
  Choice(name = "two", value = 2),
  Choice(name = "three", value = 3),
  Choice(name = "older than three", value = 4)
])

  async def introduce(
    self,
    interaction: discord.Interaction,
    name: str,
    age: int) -> None:
  
    await interaction.response.send_message(
    f"My name is {name} and I am {age} years old!")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    introduce(bot)
  )