import discord, os, random
import instaloader
from instaloader import Profile
from discord import File


from discord.ext.commands import Cog, Bot, Context, command

class PicturesCog(Cog):
    def __init__(self, bot:Bot) :
        self.bot = bot

    
    @command(name='pictures')
    async def pictures(self, ctx:Context, args):
        user_name = args.join('')
        L=instaloader.Instaloader()

        with open('./data/login_instagram') as f:
            user_name = f.readline()
            user_passwort = f.readlines()


        USER = user_name 
        PASSWORD = user_passwort[0]

        L.login(USER, PASSWORD)         # login
        
        
        profile = Profile.from_username(L.context, user_name)

        
        post = profile.get_posts()
        
        
        L.posts_download_loop(post, 'pictures')
     
    
    @command(name='get')
    async def get(self, ctx:Context):
        file = random.choice(os.listdir('./pictures'))
        while file.endswith('.txt'):
            file = random.choice(os.listdir('./pictures'))
        with open('pictures/'+file) as _:            
            await ctx.reply(file = File('pictures/'+ file))
        
