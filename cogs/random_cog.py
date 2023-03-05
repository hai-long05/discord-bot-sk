from dis import disco
from math import *
from time import time
from typing import List
from asyncio import sleep
from os import name, remove as rm_file
from string import ascii_letters
from random import choice, randrange, shuffle, sample
from math import *
from pynput.keyboard import Key, Controller


from yt_dlp import YoutubeDL
from mathgenerator import mathgen
from cv2 import RETR_CCOMP, VideoCapture, imwrite
from discord.ext.commands import Cog, Bot, Context, command
from discord import Member, Embed, File, VoiceChannel, Role, FFmpegPCMAudio, Message, message
from yt_dlp.extractor.lazy_extractors import NetEaseMusicMvIE


class RandomCog(Cog):
    def __init__(self, bot: Bot) :
        self.bot = bot

    @command(name='lk', aliases=['leistungskurs'])
    async def lk(self, ctx: Context):
        self.task, self.solutions = choice([
            mathgen.basic_algebra,
            mathgen.addition,
            mathgen.exponentiation,
        ])()

        return await ctx.send(self.task)


    @command(name='solution')
    async def solution(self, ctx: Context, arg):
        if arg == self.solutions:
            await ctx.reply("Correct answer \n access to rank \'Leistungskurs\'")
            for roles in ctx.guild.roles:
                if roles.id == 930170432093581313:
                    role_to_add = roles
            await ctx.author.add_roles(role_to_add)
            self.task = ''
            self.solutions = ''
            await sleep(60)
            await ctx.author.remove_roles(role_to_add)


    @command(name='unterricht')
    async def unterricht(self, ctx: Context, member: Member, seconds: str):
        try:
            seconds = int(seconds)

            for role in ctx.guild.roles:
                if role.id == 930170432093581313:
                    lk_role = role
            
            if not isinstance(role, Role):
                await ctx.reply('Leistungskurs role not found.')

            await member.add_roles(lk_role)

            prev_channel = member.voice.channel
            lk_channel: VoiceChannel = self.bot.get_channel(930095947294322728)

            await member.move_to(lk_channel)

            await sleep(seconds)

            await member.remove_roles(lk_role)
            await member.move_to(prev_channel)

        except ValueError:
            await ctx.reply('This is not a valid time.')
    
    @unterricht.error
    async def unterricht_error(self, ctx: Context, error):
        await ctx.reply(error)
