import asyncio
import discord

from asyncio import sleep
from discord.ext.commands import Cog, Bot, command, Context

class CountingCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:

            return

     

        with open('data/counting_channel', 'r') as f:
            
            channel_id = f.read()


        if channel_id == '':

            return
        
        channel = self.bot.get_channel(id=int(channel_id))

        if message.channel.id == channel.id:


            try:

                enter_num = int(message.content)

            except:

                await self.clear(channel)

                await channel.send('You can now start from 0')
                
                return
            
            with open('data/counting', 'r') as f:

                num = f.readline()

            num = int(num) 

            if enter_num != num:
                
                with open('data/counting_channel', 'w+') as f:

                    save_channel = f.readline()
                    print(save_channel)

                await channel.send('Game over you failed. The messages in this channel will be deleted in:')

                await sleep(1)

                await channel.send('3')

                await sleep(1)

                await channel.send('2')
                
                await sleep(1)

                await channel.send('1')

                await self.clear(channel)

                await channel.send('You can now start from 0')

                with open('data/counting_channel', 'w+') as f:

                    f.writelines(save_channel)

            else: 

                num += 1

                with open('data/counting', 'w') as f:

                    f.writelines(str(num))


    @command(alias='counting')
    async def counting(self, ctx: Context):
        await sleep(5)
        channel = ctx.channel.id
        with open('data/counting', 'w+') as f:
            f.writelines('0')
        with open('data/counting_channel', 'w+') as f:
            f.write(str(channel))
        await ctx.send('The counting channel initiated. You can now start counting from 0')
        pass

    
    async def clear(self, channel):
        
        await channel.purge()
        with open('data/counting', 'w+') as f:
            f.writelines('0')


    @command(name="clear")
    async def clear_channel(self, ctx: Context):
        messages = await ctx.channel.history(limit=10).flatten()
        print(messages)
        while messages != []:
            await ctx.channel.purge()
            
        
    