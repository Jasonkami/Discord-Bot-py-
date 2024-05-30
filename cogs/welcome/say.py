import discord
from discord import app_commands
from discord.app_commands import Choice, Command
from discord.ext import commands


class say(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(
    name = "say",
    description = "Say Something!")

  @app_commands.describe(
    thing_to_say = "What should I say?"
  )
  async def say(
    self,
    interaction: discord.Interaction,
    thing_to_say: str):
    await interaction.response.send_message(
      f"{interaction.user.name} said: `{thing_to_say}`"    
    )

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    say(bot)
  )