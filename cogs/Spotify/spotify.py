import discord
from discord import app_commands, Spotify
from discord.ext import commands

class SpotifyCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="spotify",
        description="Shows the current song that is playing on Spotify."
    )
    async def spotify(self, interaction: discord.Interaction, user: discord.Member) -> None:
        for activity in user.activities:
            if isinstance(activity, Spotify):
                embed = discord.Embed(
                    title=f"{user.name}'s Spotify",
                    description=f"Listening to {activity.title}",
                    color=0x1DB954  # Typical Spotify green color
                )
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Artist", value=activity.artist)
                embed.add_field(name="Album", value=activity.album)
                if activity.created_at is not None:
                    embed.set_footer(text=f"Song started at {activity.created_at.strftime('%H:%M')}")
                else:
                    embed.set_footer(text="Song started time not available")

                await interaction.response.send_message(embed=embed)
                return  # Exit after sending the message

        await interaction.response.send_message(f"{user.name} is not listening to Spotify.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        SpotifyCog(bot)
    )