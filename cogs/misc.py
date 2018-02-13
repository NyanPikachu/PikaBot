import discord
from discord.ext import commands
import random
from random import randint
class misc:
    '''Miscellaneous commands that are fun!'''
    def __init__(self, bot):
        self.bot = bot
        
    
    
    @commands.command()
    async def hug(self, ctx, user: discord.Member=None):
        """hugs a user"""
        if not user:
            await ctx.send(f"Please mention someone for this command to work {ctx.author.mention}" )
        embed = discord.Embed(title="Hug!".format(user.name), description= f"{ctx.author} has sent {user} a hug !", color=0xffb6c1)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)
        
    @commands.command(hidden=True)
    async def say(self, ctx, *, msg: str):
        """owner only command- print a message"""
        await ctx.message.delete()
        await ctx.send(msg)
    
    @commands.command()
    async def coinflip(self, ctx):
        """Flips a coin!"""
        flip = random.choice(["Heads", "Tails"])
        await ctx.send(flip)
    
    @commands.command()
    async def embedsay(self, ctx, *, body: str):
        '''Send a simple embed'''
        em = discord.Embed(description=body, color=discord.Member.color)
        await ctx.send(embed=em)
        
    @commands.command(name='presence', hidden=True)
    @commands.is_owner()
    async def _presence(self, ctx, type=None, *, game=None):
        '''Change the bot's presence'''
        if type is None:
            await ctx.send(f'Usage: `{ctx.prefix}presence [game/stream/watch/listen] [message]`')
        else:
            if type.lower() == 'stream':
                await self.bot.change_presence(game=discord.Game(name=game, type=1, url='https://www.twitch.tv/a'), status='online')
                await ctx.send(f'Set presence to. `Streaming {game}`')
            elif type.lower() == 'game':
                await self.bot.change_presence(game=discord.Game(name=game))
                await ctx.send(f'Set presence to `Playing {game}`')
            elif type.lower() == 'watch':
                await self.bot.change_presence(game=discord.Game(name=game, type=3), afk=True)
                await ctx.send(f'Set presence to `Watching {game}`')
            elif type.lower() == 'listen':
                await self.bot.change_presence(game=discord.Game(name=game, type=2), afk=True)
                await ctx.send(f'Set presence to `Listening to {game}`')
            elif type.lower() == 'clear':
                await self.bot.change_presence(game=None)
                await ctx.send('Cleared Presence')
            else:
                await ctx.send('Usage: `.presence [game/stream/watch/listen] [message]`')
 
        
def setup(bot):
    bot.add_cog(misc(bot))
