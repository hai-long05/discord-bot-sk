from discord import Member, VoiceChannel
from asyncio import sleep
from discord.ext.commands import Cog, Context, command

class LessonCog(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.duration = 0
        self.member_roles = []
        self.member: Member


    @command(name='lesson')
    async def lesson(self, ctx, member_id, duration):
        member = await self.check_for_id(ctx, member_id)

        channel = ctx.author.voice.channel
        
        teacher = ctx.message.author.id

        if (str(teacher) == member):
            await ctx.reply('You can\'t teach yourself')

            return 
        
        room: VoiceChannel = self.bot.get_channel(1055206431256752298)

        duration = int(duration)

        for mem in ctx.guild.members:

            if (mem.id == int(member)):
                member = mem
                break

        for mem in ctx.guild.members:

            if (mem.id == int(teacher)):
                teacher = mem
                break

        self.member_roles = member.roles

        student = ctx.guild.get_role(1055113243829473391)

        await member.edit(roles=[student])

        await member.move_to(room)

        await teacher.move_to(room)

        await sleep(duration)

        await member.edit(roles=self.member_roles)

        try:
            await member.move_to(channel)

            await teacher.move_to(channel)

        except:
            
            await ctx.reply('unable to move back \n reason: not connected to any voice channel')

        

    @command(name='over')
    async def over(self, ctx: Context):
        pass
        # await member.edit

    async def check_for_id(self, ctx: Context, member_id):
        if '@' in member_id and '&' not in member_id: # making sure that the inserted id is a member id
            
            member: Member = member_id.replace('<', '').replace('!', '').replace('@', '').replace('>', '')
            return member

        else:

            await ctx.reply('This ist not a member.')
            return None


