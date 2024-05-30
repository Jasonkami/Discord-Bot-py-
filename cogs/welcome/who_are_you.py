import discord
from discord import app_commands
from discord.app_commands import Choice, Command
from discord.ext import commands


class who_are_you(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(
    name = "who_are_you",
    description = "I will tell you something about myself!")

  async def who_are_you(
    self,
    interaction: discord.Interaction):

    await interaction.response.send_message(
      f"Hey {interaction.user.mention}! I am a discord bot developed by the user 'Jasonkami.'!")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    who_are_you(bot)
  )