from discord import Member
from string import ascii_letters
from random import choice, sample
from discord.ext.commands import Context, Bot, Cog, command

class GeneratorCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        

    @command(name='randomteamgen')
    async def randomteamgen(self, ctx: Context):

        channel = ctx.author.voice.channel
        members = channel.members # get members in channel
        members_in_channel = []
        team_1 = []

        for members in ctx.guild.members: # get all the member-ids

            if int(members) == members.id:

                members_in_channel.append(members.name) # store all member in a list

        n = len(members_in_channel) // 2 # half of all members in the channel | if uneven number the second team will have more members because // 2 complement the decimal number

        for _ in range(n): # choice of the random teams throught random choosing members from list

            name = choice(members_in_channel)
            team_1.append(name)
            Idx = members_in_channel.index(name)
            members_in_channel.pop(Idx)

        await ctx.reply(f'team 1: {team_1} \nteam 2: {members_in_channel}')


    @command(name='generate')
    async def generatepasswort(self, ctx: Context, arg):
        member: Member = await ctx.author.create_dm()
        letters = ascii_letters # get all letters
        symbols =  '+*~#-_.:,;<>|!§$%&/()={[]}'
        numbers = '1234567890'
        all_symbols = letters + symbols + numbers # combine all letters, symbols and numbers to one string to random choose 
        length = int(arg)
        if length > 88:
            return await ctx.reply('can\'t generate password too much characters')
        password_list = sample(all_symbols, length)
        password = ''.join(password_list)
        await member.send(password)