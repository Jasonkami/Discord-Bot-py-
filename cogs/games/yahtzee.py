import asyncio
import datetime
import os
from itertools import cycle
import aiohttp
import discord
import tasks
import random
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands, tasks

class Yahtzee:
    def __init__(self):
        self.dice = [0] * 5
        self.rolls = 3
        self.score = 0
        self.categories = {
            '1': None,
            '2': None,
            '3': None,
            '4': None,
            '5': None,
            '6': None,
            'three_of_a_kind': None,
            'four_of_a_kind': None,
            'full_house': None,
            'small_straight': None,
            'large_straight': None,
            'yahtzee': None,
            'chance': None
        }

    def roll_dice(self, keep=None):
        if keep is None:
            keep = [False] * 5
        for i in range(5):
            if not keep[i]:
                self.dice[i] = random.randint(1, 6)
        self.rolls -= 1

    def score_category(self, category):
        if category not in self.categories or self.categories[category] is not None:
            return False

        if category in ['1', '2', '3', '4', '5', '6']:
            self.categories[category] = sum(d for d in self.dice if d == int(category[0]))
        elif category == 'three_of_a_kind' and self._has_n_of_a_kind(3):
            self.categories[category] = sum(self.dice)
        elif category == 'four_of_a_kind' and self._has_n_of_a_kind(4):
            self.categories[category] = sum(self.dice)
        elif category == 'full_house' and self._has_full_house():
            self.categories[category] = 25
        elif category == 'small_straight' and self._has_straight(4):
            self.categories[category] = 30
        elif category == 'large_straight' and self._has_straight(5):
            self.categories[category] = 40
        elif category == 'yahtzee' and self._has_n_of_a_kind(5):
            self.categories[category] = 50
        elif category == 'chance':
            self.categories[category] = sum(self.dice)
        else:
            return False

        self.score += self.categories[category]
        return True

    def _has_n_of_a_kind(self, n):
        return any(self.dice.count(x) >= n for x in set(self.dice))

    def _has_full_house(self):
        unique_counts = set(self.dice.count(x) for x in set(self.dice))
        return unique_counts == {2, 3}

    def _has_straight(self, length):
        unique_dice = sorted(set(self.dice))
        for i in range(len(unique_dice) - length + 1):
            if unique_dice[i + length - 1] - unique_dice[i] == length - 1:
                return True
        return False

class YahtzeeCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.game_sessions = {}

    @app_commands.command(name = "yahtzee_help", description = "Shows the help menu for Yahtzee!")
    async def yahtzee_help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="How to play Yahtzee", description="The title says it all!", color=discord.Color.random())
        embed.add_field(name="Rules", value="This is a single/multi player Yahtzee game.\nThe game consists of thirteen rounds. Each round begins with the rolling of five dice. The player has a total of 3 rolls within the round. The player can choose certain dice to hold their values during a reroll by 'keeping' them. This is done by using the 'keep' function within the players next roll-command.\nEach round must be scored in one and only one of the following categories.\n[For a full explanation, check out this pdf file](https://www.hasbro.com/common/instruct/yahtzee.pdf)", inline=False)
        embed.add_field(name="Keep-Mechanic: (IMPORTANT)", value="If you want to keep a dice or multiple dices to only reroll the ones you are not willing to keep, you have to use the 'keep' function within the roll-command. You have to put the numbers of the dices that you want to keep into the the 'keep' field seperated by commas like this: keep: 1, 3, 5'.", inline=False)
        embed.add_field(name="Basic Categories", value="Ones: Sum of the ones displayed at time the score is entered.\n1 1 1 1 4 would receive a score of 4.\n\nTwos: Sum of the twos displayed at time the score is entered.\n2 2 6 3 2 would receive a score of 6.\n\nThrees: Sum of the threes displayed at time the score is entered.\n3 6 2 2 2 would receive a score of 3.\n\nFours: Sum of the fours displayed at time the score is entered.\n2 1 2 4 4 would receive a score of 8.\n\nFives: Sum of the fives displayed at time the score is entered.\n1 5 6 5 1 would receive a score of 10.\n\nSixes: Sum of the sixes displayed at time the score is entered.\n1 3 6 6 5 would receive a score of 12.", inline=False)
        embed.add_field(name="Advanced Categories", value="Three of a kind: Sum of all of the dice provided three of them are the same; zero otherwise.\n6 6 5 6 4 would receive a score of 27.\n\nFour of a kind: Sum of all of the dice provided four of them are the same; zero otherwise.\n5 5 5 5 1 would receive a score of 21.\n\nFull house: 25 points provided that one has three-of-a-kind and the other two dice are a pair (are the same).\n5 6 6 5 6 would receive a score of 25.\n\nSmall straight: 30 points provided four of the dice have consecutive values; zero otherwise.\n4 3 6 4 5 would receive a score of 30.\n\nLarge straight: 40 points provided all five dice have consecutive values; zero otherwise.\n4 3 6 5 2 would receive a score of 40.\n\nYahtzee: 50 points provided all five dice have the same value; zero otherwise.\n3 3 3 3 3 would receive a score of 50.\n\nChance: Sum of all of the dice.\n5 6 4 6 4 would receive a score of 25.", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="yahtzee_start", description="Starts a new Yahtzee game.")
    async def start(self, interaction: discord.Interaction):
        user_id = discord.Member.id
        if user_id in self.game_sessions:
            await interaction.response.send_message("You already have an active game. Use !yahtzee_end to finish your current game.")
        else:
            self.game_sessions[user_id] = Yahtzee()
            await interaction.response.send_message("Started a new game of Yahtzee! Use !yahtzee_roll to roll the dice.")

    @app_commands.command(name="yahtzee_roll", description="Rolls the dice for the current game.")

    #@app_commands.choices(keep = [
        #Choice(name = "None", value = "none"),
        #Choice(name = "First dice", value = "0"),
        #Choice(name = "Second dice", value = "1"),
        #Choice(name = "Third dice", value = "2"),
        #Choice(name = "Fourth dice", value = "3"),
        #Choice(name = "Fifth dice", value = "4")

    #])
    
    async def roll(self, interaction: discord.Interaction, 
                   keep: str = ""
                  ):
        user_id = discord.Member.id
        if user_id not in self.game_sessions:
            await interaction.response.send_message("You don't have an active game. Use !yahtzee_start to begin a new game.")
            return

        game = self.game_sessions[user_id]
        keep_list = [False] * 5
        if keep:
            keep_indices = [int(i) for i in keep if i.isdigit() and 1 <= int(i) < 6]
    
            for i in keep_indices:
                i-=1
                keep_list[i] = True

        if game.rolls > 0:
            game.roll_dice(keep_list)
            await interaction.response.send_message(f'Rolled: {game.dice}\nRolls remaining: {game.rolls}\nRemember to keep some dice if you want to!')
        else:
            await interaction.response.send_message("No rolls remaining. Use !yahtzee_score <category> to score this round.")

    @app_commands.command(name="yahtzee_score", description="Scores the current round.")

    @app_commands.choices(category = [
        Choice(name = "Ones", value = "1"),
        Choice(name = "Twos", value = "2"),
        Choice(name = "Threes", value = "3"),
        Choice(name = "Fours", value = "4"),
        Choice(name = "Fives", value = "5"),
        Choice(name = "Sixes", value = "6"),
        Choice(name = "Three of a Kind", value = "three_of_a_kind"),
        Choice(name = "Four of a Kind", value = "four_of_a_kind"),
        Choice(name = "Full House", value = "full_house"),
        Choice(name = "Small Straight", value = "small_straight"),
        Choice(name = "Large Straight", value = "large_straight"),
        Choice(name = "Yahtzee", value = "yahtzee"),
        Choice(name = "Chance", value = "chance")
    ])
    
    async def score(self, interaction: discord.Interaction, category: str):
        user_id = discord.Member.id
        if user_id not in self.game_sessions:
            await interaction.response.send_message("You don't have an active game. Use !yahtzee_start to begin a new game.")
            return

        game = self.game_sessions[user_id]
        if game.score_category(category):
            await interaction.response.send_message(f"Scored {category}. Your total score is now {game.score}.")
            game.rolls = 3
        else:
            await interaction.response.send_message("Invalid category or already scored. Please choose another category.")

    @app_commands.command(name="yahtzee_end", description="Ends the current Yahtzee game.")
    async def end(self, interaction: discord.Interaction):
        user_id = discord.Member.id
        if user_id in self.game_sessions:
            game = self.game_sessions.pop(user_id)
            await interaction.response.send_message(f"Game ended. Your final score was {game.score}.")
        else:
            await interaction.response.send_message("You don't have an active game.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(YahtzeeCog(bot))