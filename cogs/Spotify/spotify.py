import sys
#import spotipy
#from spotipy.oauth2 import SpotifyClientCredentials

import discord
from discord import app_commands
from discord.ext import commands
import Spotify

# get spotify credentials from environment variables
#client_credentials_manager = SpotifyClientCredentials()
#sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# open private key file
key_file = open('./discord_key.txt', 'r')
if not key_file:
    print('File discord_key.txt can\'t be found')
    sys.exit(0)

# read private key from file
api_key = key_file.read().splitlines()[0]
if not api_key:
    print('No API key in discord_key.txt')
    sys.exit(0)

class SpotifyCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    #@app_commands.command(name="spotify", description="Search something!")
    
    #async def spotify(self, interaction: discord.Interaction,  message):
        
        #if message.content.startswith('.song '):
            #results = sp.search(q=message.content[6:], limit=1, type='track') 
            #url = 'https://open.spotify.com/track/{}'.format(results['tracks']['items'][0]['id'])
            #await interaction.response.send_message(content=url)
        #elif message.content.startswith('.track '):
            #results = sp.search(q=message.content[7:], limit=1, type='track') 
            #url = 'https://open.spotify.com/track/{}'.format(results['tracks']['items'][0]['id'])
            #await interaction.response.send_message(content=url)
        #elif message.content.startswith('.album '):
            #results = sp.search(q=message.content[7:], limit=1, type='album') 
            #url = 'https://open.spotify.com/album/{}'.format(results['albums']['items'][0]['id'])
            #await interaction.response.send_message(content=url)
        #elif message.content.startswith('.artist '):
            #results = sp.search(q=message.content[8:], limit=1, type='artist') 
            #url = 'https://open.spotify.com/artist/{}'.format(results['artists']['items'][0]['id'])
            #await interaction.response.send_message(content=url)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        SpotifyCog(bot)
    )