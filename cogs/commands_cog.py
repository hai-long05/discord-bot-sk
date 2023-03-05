import pytz
import disnake
#import datetime

from datetime import datetime
from discord import Member, Embed
from discord.utils import get
from discord.ext.commands import Context, Cog, Bot, command


class CommandsCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f'Name: {self.bot.user}')
    
    @command(name='role')
    async def role(self, ctx: Context, member_id, role_id):
        member = await self.check_for_id(ctx, member_id) # check if the entered member is an actual member

        if member == None:

            return        
        role = await self.check_for_role(ctx, role_id) # check if it's a valid role 

        if role == None:

            return await ctx.reply('Invalid role')


        for members in ctx.guild.members:

            if int(member) == members.id:

                member_to_add = members
                break

        for roles in ctx.guild.roles:

            if int(role) == roles.id:

                role_to_add = roles
                break

        print (ctx.author.roles)

        for roles in ctx.author.roles: # check for autorisation

            if roles.id == 930170432093581313:

                await member_to_add.add_roles(role_to_add)
                await ctx.reply(f'The role \'{role_to_add}\' has been added to the member {member_to_add}')

        else:

            await ctx.reply('Missing Permission')


    async def check_for_id(self, ctx: Context, member_id):
        if '@' in member_id and '&' not in member_id: # making sure that the inserted id is a member id
            
            member: Member = member_id.replace('<', '').replace('!', '').replace('@', '').replace('>', '')
            return member

        else:

            await ctx.reply('This ist not a member.')
            return None


    async def check_for_role(self, ctx, role_id):
        if '&' in role_id:

            member = role_id.replace('<', '').replace('&', '').replace('@', '').replace('>', '')
            return member

        else:

            return None


    @command(name='userinfo')
    async def userinfo(self, ctx: Context, member_id):


        id = await self.check_for_id(ctx, member_id)

        # member mit dieser id aus allen membern
        member = get(self.bot.get_all_members(), id=int(id))

        # await ctx.reply(f'This is a member. Name: {member.display_name}')

        de = pytz.timezone('Europe/Berlin')
        embed = Embed(title=f'> Userinfo für {member.display_name}',
                        description='', color=0x4cd1f7, timestamp=datetime.now().astimezone(tz=de))

        embed.add_field(
            name='Name', value=f'```{member.name}#{member.discriminator}```', inline=True)
        embed.add_field(
            name='Bot', value=f'```{("Ja" if member.bot else "Nein")}```', inline=True)
        embed.add_field(
            name='Nickname', value=f'```{(member.nick if member.nick else "Nicht gesetzt")}```', inline=True)
        embed.add_field(name='Server beigetreten',
                        value=f'```{member.joined_at}```', inline=True)
        embed.add_field(name='Discord beigetreten',
                        value=f'```{member.created_at}```', inline=True)
        embed.add_field(
            name='Rollen', value=f'```{len(member.roles) - 1}```', inline=True)
        embed.add_field(name='Höchste Rolle',
                        value=f'```{member.top_role.name}```', inline=True)
        embed.add_field(
            name='Farbe', value=f'```{member.color}```', inline=True)
        embed.add_field(
            name='Booster', value=f'```{("Ja" if member.premium_since else "Nein")}```', inline=True)
        embed.set_footer(
            text=f'Angefordert von {ctx.author.name} • {ctx.author.id}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)



    @command(name='request')
    async def request(self, ctx: Context):
        game = ctx.author.activities[0].name
        for member in ctx.guild.members:
            if not member.bot and member != ctx.author:
                await member.create_dm()
                await member.send(f'Hast du bock mit {game} zu spielen?')

    
    @command(name='ban')
    async def ban(self, ctx: Context, member_id):
        member_to_ban = await self.check_for_id(ctx, member_id)
        for member in ctx.guild.members:
            if member.id == int(member_to_ban):
                await ctx.reply(f'{member} has been banned')
                return await member.ban()
    

    @command(name='kick')
    async def kick(self, ctx: Context, member_id):
        member_to_kick = await self.check_for_id(ctx, member_id)
        for member in ctx.guild.members:
            if member.id == int(member_to_kick):
                await ctx.reply(f'{member} has been kick')
                return await member.kick()

    @command(name='commands')
    async def commands(self, ctx: Context):

        de = pytz.timezone('Europe/Berlin')

        embed = Embed(title="LIST OF ALL COMMANDS",
                        description='', color=0x4cd1f7, timestamp=datetime.now().astimezone(tz=de))
        # embed.add_field(name = ) 
        await ctx.reply(embed=embed)