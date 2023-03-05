from ast import alias
from random import choice, shuffle, randrange
from discord.ext.commands import Cog, Bot, Context, command

class GamesCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        self.letter = ''
        self.unknown_list = []
        self.guess_count = 0
        self.letter_list = []
        self.word = ''


    @command(name='hangman')
    async def hangman(self, ctx: Context):
        a = ''

        if self.letter_list != []:
            
            return await ctx.reply('Their is already a hangman game on the server') # prevent 2 games

        word = self.random_line() # get random word
        self.letter = ''.join(word) 
        self.letter_list = list(self.letter) # split word into list of letters
        
        for _ in range (len(self.letter)): # generate place holders for the numbers of letters | using _ cause the variable is not needed

            a += '-'

        await ctx.reply(f'Game started\n{a}')


    @command(name='answer')
    async def answer(self, ctx: Context, arg):     
        if len(arg) > 1:

            if arg == self.letter: # if the answer is correct reset all list and count | new game can be started

                self.letter_list = []
                self.unknown_list = []
                self.guess_count = 0
                return await ctx.reply('correct answer')

            else:

                return await ctx.reply('incorrect answer')

        a = 0

        if self.unknown_list == []: # unknown_list is a helper list that could be change each guess | needed to store the already guessed letter(s)

            for i in self.letter_list:

                if i == arg: # if the letter is in the word the place holders will be replaced with the correct letter | if the letter is in the word mulitple time it will also work

                    self.unknown_list.append(arg) 

                else:

                    self.unknown_list.append('-')

        else: 

            for i in self.letter_list:

                if i == arg:

                    self.unknown_list[a] = arg
                else:

                    if self.unknown_list[a] == '-':

                        self.unknown_list[a] = '-'

                    else:

                        self.unknown_list[a] = self.unknown_list[a]

                a += 1

        self.guess_count += 1

        if self.guess_count == 7: # if you guessed 7 times incorrectly the game is over and you will lose

            self.letter_list = []
            self.unknown_list = []
            self.guess_count = 0
            return await ctx.reply('You lose')

        answer_string = ''.join(self.unknown_list) # turn list into word to reply in chat
        await ctx.reply(answer_string)


    @command(name='scramble')
    async def scramble(self, ctx: Context):
        if self.word == '': # check if there is already a game

            self.word = self.random_line()
            list_word = list(self.word)
            shuffle(list_word) # 'scramble'/mix the word 
            msg = ''.join(list_word)
            await ctx.send(f'The word is: {msg}')

        else:

            await ctx.send('already a game started')


    @command(name='guess')
    async def guess(self, ctx: Context, arg):
        if arg == self.word:

            self.word = ''
            await ctx.reply('correct answer')

        return


    def random_line(self): # get random word
        file = open('./data/words', 'r')
        lines = file.read()
        words = lines.splitlines()
        return choice(words)


    @command(alias='roll')
    async def dice(self, ctx: Context):
        await ctx.reply (f'You rolled: {randrange(1, 7)}')


    async def reset(self):
        self.number_of_run += 1
        if self.list_length == self.number_of_run:
            self.number_of_run = 0
            self.list_length = 0
            self.left_list_symbol = ''
            self.right_list_symbol = ''
            self.count = 0
        