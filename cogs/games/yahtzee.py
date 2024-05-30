import random
import discord
from discord import app_commands
from discord.ext import commands

class Yahtzee:
    def __init__(self):
        self.dice = [0] * 5
        self.rolls = 3
        self.score = 0
        self.categories = {
            'ones': None,
            'twos': None,
            'threes': None,
            'fours': None,
            'fives': None,
            'sixes': None,
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

        if category in ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']:
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

    @app_commands.command(name="yahtzee_start")
    async def start(self, interaction: discord.Interaction):
        user_id = discord.Member.id
        if user_id in self.game_sessions:
            await interaction.response.send_message("You already have an active game. Use !yahtzee_end to finish your current game.")
        else:
            self.game_sessions[user_id] = Yahtzee()
            await interaction.response.send_message("Started a new game of Yahtzee! Use !yahtzee_roll to roll the dice.")

    @app_commands.command(name="yahtzee_roll")
    async def roll(self, interaction: discord.Interaction, keep: str = ""):
        user_id = discord.Member.id
        if user_id not in self.game_sessions:
            await interaction.response.send_message("You don't have an active game. Use !yahtzee_start to begin a new game.")
            return

        game = self.game_sessions[user_id]
        keep_list = [False] * 5
        if keep:
            keep_indices = [int(i) for i in keep if i.isdigit() and 0 <= int(i) < 5]
            for i in keep_indices:
                keep_list[i] = True

        if game.rolls > 0:
            game.roll_dice(keep_list)
            await interaction.response.send_message(f'Rolled: {game.dice}\nRolls remaining: {game.rolls}')
        else:
            await interaction.response.send_message("No rolls remaining. Use !yahtzee_score <category> to score this round.")

    @app_commands.command(name="yahtzee_score")
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

    @app_commands.command(name="yahtzee_end")
    async def end(self, interaction: discord.Interaction):
        user_id = discord.Member.id
        if user_id in self.game_sessions:
            game = self.game_sessions.pop(user_id)
            await interaction.response.send_message(f"Game ended. Your final score was {game.score}.")
        else:
            await interaction.response.send_message("You don't have an active game.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(YahtzeeCog(bot))