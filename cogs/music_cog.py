from asyncio.tasks import wait
from os import error
from sys import is_finalizing
import discord
import asyncio
import random
import yt_dlp

from discord import voice_client
#from discord.ext.commands.context import Context
from discord.ext.commands.errors import ChannelNotFound
from discord.ext.commands import Cog, Bot, Context, command


class MusicCog(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'} # Setting for youtube mp3 download
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'} # Play Settings in Channel

        self.vc = ""
        self.voice_channel = ""


    def search_yt(self, item):
        with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0] # search Youtube for the first entry that comes up with the song title
            except Exception:
                return False
             
        return {'source': info['formats'][3]['url'], 'title': info['title']} # return source and title in a dictionary


    async def play_next(self): # Funktion to play music continiously
        self.music_queue.pop(0)
        if len(self.music_queue) > 0:            
            source = self.search_yt(self.music_queue[0])                    
            self.vc.play(discord.FFmpegPCMAudio(source['source'], **self.FFMPEG_OPTIONS))
            while self.vc.is_playing():
                await asyncio.sleep(2)
            if not self.vc.is_connected() or self.vc == '':
                return
            await self.play_next()
        else:
            await asyncio.sleep(10)
            await self.vc.disconnect()
            self.vc = ""
            return 
    

    @command(name='p')
    async def play(self, ctx:Context, *args):
        try:
            if not self.vc.is_connected(): # if bot get disconnected the queue get cleared
                self.music_queue = []
        except:
            print(error)
        song_title = " ".join(args) 
        if len(self.music_queue) > 0: # if there are already songs playing the song gets added to the queue
            self.music_queue.append(song_title)
            await ctx.reply('Song added to QUEUE')
        else:
            song_title = " ".join(args)
            self.music_queue.append(song_title)
            voice_state = ctx.author.voice
            if voice_state is None: # check if the user is connected to voice channel
                return await ctx.reply("You need to be connected to a voice channel")
            else:
                self.voice_channel = ctx.author.voice.channel
                await ctx.reply("request received")
            source = self.search_yt(self.music_queue[0]) # get source         
            print(source)
            self.vc = await self.voice_channel.connect() # bot connect to user voice channel
            self.vc.play(discord.FFmpegPCMAudio(source['source'], **self.FFMPEG_OPTIONS)) # play the song with the given settings
            while self.vc.is_playing(): # make sure the song gets entirely played
                await asyncio.sleep(5)
            if not self.vc.is_connected() or self.vc == '':
                return
            await self.play_next() # play next song if there are no song in the queue, disconnect from channel


    @command(name='q')
    async def queue(self, ctx:Context):
        if self.music_queue == []:
            return await ctx.reply('Nothing in the queue')
        a = 0
        q = ""
        for i in self.music_queue:
            if a == 0:
                q += i + '\n'
            elif a == 1:
                q += '--------------' + '\n' + str(a) + ')' + '    ' + i
            else:
                q += str(a) + ')' + '    ' + i + '\n'
            a += 1

        await ctx.reply(f'currently playing:\n{q}')

    
    @command(name='skip')
    async def skip(self, ctx:Context):
        self.vc.stop()
        await self.play_next()


    @command(name='leave')
    async def leave(self, ctx:Context):
        await self.vc.disconnect()
        await ctx.reply('Bot left the channel.')
        await asyncio.sleep(6)
        self.music_queue = []
        self.vc = ""

    
    @command(name='Blackpink')
    async def Blackpink(self, ctx:Context):
        songs = ['How You Like That', 'DDU-DU DDU-DU', 'Kill This Love', 'AS IF IT\'S YOUR LAST', 'BOOMBAYAH', 'PLAYING WITH FIRE', 'STAY', 'Lovesick Girls']
        number = random.randint(0,len(songs)-1)
        song_title = songs[number]
        await self.play(ctx, song_title)


    
    @command(name='vibe')
    async def vibe(self, ctx:Context):
        song_title = self.random_line()
        await self.play(ctx, song_title)


    @command(name='addtolist')
    async def addtolist(self, ctx:Context, *args):
        title = " ".join(args)
        title = title.lower()
        file1 = open('./data/songs', 'r')
        lines = file1.read()
        songs = lines.splitlines()
        for l in songs:
            if l == title:
                return await ctx.reply('Already in the list')
        file = open('./data/songs', 'a', encoding='utf-8')
        file.write('{}\n'.format(title))
        file.close()
    

    def random_line(self):
        file = open('./data/songs', 'r')
        lines = file.read()
        songs = lines.splitlines()
        return random.choice(songs)


