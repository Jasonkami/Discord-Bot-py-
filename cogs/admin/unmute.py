import datetime
from os import error

import discord
import discord.utils
from discord import app_commands
from discord.app_commands import Choice, Command
from discord.ext import commands


class unmute(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(
    name = "unmute",
    description = "Unmutes someone! (Admin Only)")

  @commands.has_permissions(mute_members = True, manage_guild = True, manage_permissions = True, manage_roles = True)

  @app_commands.checks.has_any_role(
    "Admin",
    "Moderator",
    "Owner"
  )

  @app_commands.describe(
    user="The user to unmute")

  async def unmute(
    self,
    interaction: discord.Interaction,
    user: discord.Member):
    
    await user.edit(timed_out_until=None)
    await interaction.response.send_message(
        f"{user.name} has been unmuted!"
    )

  @unmute.error
  async def timeoutError(
      self,
      interaction: discord.Interaction,
      error: app_commands.AppCommandError
  ):
      if isinstance(error, app_commands.MissingRole):
          await interaction.response.send_message(
              "You do not have the required role to use this command!",
              ephemeral=True
          )
      else:
        raise error

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    unmute(bot)
  )