import discord
from discord import app_commands
from discord.app_commands import Choice, Command
from discord.ext import commands


class hello(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(
    name = "hello",
    description = "Say hello!")

  async def hello(
    self,
    interaction: discord.Interaction):

    await interaction.response.send_message(
    f"Hey {interaction.user.mention}! This is a slash command!", ephemeral = True)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    hello(bot)
  )