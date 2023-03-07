#Hai Long
import discord

from discord.flags import Intents
from discord.ext.commands import Bot
from cogs.commands_cog import CommandsCog
from cogs.counting_cog import CountingCog
from cogs.generator_cog import GeneratorCog
from cogs.pictures_cog import PicturesCog
from cogs.math_cog import MathCog
from cogs.punish_cog import PunishCog
from cogs.music_cog import MusicCog
from cogs.games_cog import GamesCog
from cogs.lesson_cog import LessonCog
# from cogs.help_cog import HelpCog

def get_token():
    with open('./data/token') as f:
        token = f.readline()
    return token

bot = Bot(intents = discord.Intents.all(), command_prefix='!')


bot.add_cog(MusicCog(bot))

bot.add_cog(PicturesCog(bot))

bot.add_cog(MathCog(bot))

bot.add_cog(GamesCog(bot))

bot.add_cog(PunishCog(bot))

bot.add_cog(GeneratorCog(bot))

bot.add_cog(CommandsCog(bot))

bot.add_cog(CountingCog(bot))

bot.add_cog(LessonCog(bot))

bot.run(get_token())

