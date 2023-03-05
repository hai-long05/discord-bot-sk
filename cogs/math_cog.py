import discord
from discord.ext.commands import Cog, Context, command
from mathgenerator import mathgen

class MathCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.solutions = 0
        self.problem = ''
        
    @command(name='pi')
    async def pi(self, ctx: Context, args):
        try:
            num_digits = int(args)
        except ValueError:
            return ctx.reply('invalid input')
        with open('./data/pi') as f:
            pi = f.readlines()
        for i in range(0, num_digits, 1999):
            await ctx.reply(pi[0][i:i+2000])

    @command(name='quadratic')
    async def quadratic(self, ctx: Context):
        problem, self.solutions = mathgen.quadratic_equation()
        await ctx.reply(problem)
        print(self.solutions)


    @command(name='basic')
    async def basic(self, ctx: Context):
        self.problem, self.solutions = mathgen.basic_algebra()
        await ctx.reply(self.problem)
        print(type(self.solutions))
        print(self.solutions)
        


    @command(name='solutions')
    async def solution(self, ctx: Context, *args):
        temp = ''.join(args)
        solutions = str(temp)
        if solutions == self.solutions:
            await ctx.reply('Your answer is true')
            self.solutions = ''
        else:
            await ctx.reply('Wrong answer')


    