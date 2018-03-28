import discord
from discord.ext import commands
from ext.paginator import PaginatorSession
import clashroyale
import os
from firebase import Firebase

class Clash_Royale:
    '''Clash Royale commands to get your fancy stats here!'''
    def __init__(self, bot):
        self.bot = bot
        self.db = Firebase('https://pikabot-fa952.firebaseio.com/', auth_token="AIzaSyB48L7AFMTepuFkvoFIcauJLJrrmVaRrVQ")
        
    @commands.command()
    async def crsave(self, ctx, tag :str=None):
        if not tag:
            await ctx.send('Please provide a tag')
        try:
           f.push({'clashroyale': {str(ctx.author.id): tag}})
           await ctx.send('Tag successfully saved!. Run this command again to replace with another tag.')
        except Exception as e:
           await ctx.send(str(e))
        
    @commands.command()
    async def crprofile(self, ctx, tag: str=None):
        '''Gets your Clash Royale Profile using Tag!'''
        if not tag:
            tag = f.get({'clashroyale': {str(ctx.author.id)}})
        token = os.environ.get("CRTOKEN")
        client = clashroyale.Client(token, is_async=True)
        profile = await client.get_player(tag)
        clan = await profile.get_clan()
        em = discord.Embed(color=discord.Color.gold())
        em.title = profile.name
        em.description = f'{tag}\'s info'
        await profile.refresh()
        em.add_field(name='Favourite card:', value=profile.stats.favorite_card.name)
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Clash_Royale(bot))