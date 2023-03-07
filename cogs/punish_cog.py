from ast import alias
import os

from asyncio import sleep
from random import choice
from discord import VoiceChannel, Member
from discord.ext.commands import Cog, Bot, Context, command
from discord import FFmpegPCMAudio

class PunishCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    
    @command(name='schweigeecke')
    async def schweigeecke(self, ctx: Context, member_id):
        member = await self.check_for_id(ctx, member_id)

        for members in ctx.guild.members:

            if int(member) == members.id:

                member_to_move = members
                break

        channel: VoiceChannel = self.bot.get_channel(917036688155496448)
        await member_to_move.move_to(channel, reason='Hurensohn')


    @command(name='spam')
    async def spam(self, ctx: Context, member_id, amount,*arg):
        text = ' '.join(arg)
        member_to_spam = await self.check_for_id(ctx, member_id)

        for member in ctx.guild.members:

            if member.id == int(member_to_spam):

                await member.create_dm()

                for j in range(amount):

                    await sleep(0.5)
                    
                    await member.send(text)


    async def check_for_id(self, ctx: Context, member_id):
        if '@' in member_id and '&' not in member_id: # making sure that the inserted id is a member id

            member: Member = member_id.replace('<', '').replace('!', '').replace('@', '').replace('>', '')
            return member

        else:

            await ctx.reply('This ist not a member.')
            return None


    @command(name='rollercoaster')
    async def rollercoaster(self, ctx: Context, member_id):

        member = await self.check_for_id(ctx, member_id)

        for members in ctx.guild.members: # check if member is on the server

            if int(member) == members.id: # get the id

                member_to_move = members
                break

        vc_channels = [941028680271032352, 924788779867336734, 926179778128642128, 935153503519784980, 939547541903642684]
        for i in range(20):

            if i == 9:

                await sleep(10)

            if i == 6:

                await sleep(5)

            try: # catch the error if the member leave the channel | don't need to specify the exception cause the only exception arises when the user disconnect

                vc = choice(vc_channels)
                channel: VoiceChannel = self.bot.get_channel(vc)
                await member_to_move.move_to(channel)

            except:

                return


    @command(alias='timeout')
    async def timeout(self, ctx: Context, member: Member):
        current_channel = member.voice.channel
        channel: VoiceChannel = self.bot.get_channel(930463314469875734)
        await member.move_to(channel)
        voice_channel = member.voice.channel
        vc = await voice_channel.connect()
        source_video = choice(os.listdir('data/video/'))
        print(source_video)
        vc.play(FFmpegPCMAudio(source=f'data/video/{source_video}'))

        while vc.is_playing():

            await sleep(1)

        await member.move_to(current_channel)
        await vc.disconnect()


    @timeout.error
    async def mobbing_error(self, ctx: Context, error):
        await ctx.reply(error)