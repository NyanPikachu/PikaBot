import discord
from discord.ext import commands
from ext.paginator import PaginatorSession
import clashroyale
import os

class Clash_Royale:
    '''Clash Royale commands to get your fancy stats here!'''
    def __init__(self, bot):
        self.bot = bot
        self.token = ("c94d84443b5345d784418332e81a5d3b272f67619f2cbe5f064d3d55")
        self.client = clashroyale.Client(self.token, is_async=True)
        
    @commands.command()
    async def crprofile(self, ctx, tag: str=None):
        '''Gets your Clash Royale Profile using Tag!'''
        if not tag:
             return await ctx.send('Please provide a tag for this command')
        profile = await self.client.get_player(tag)
        clan = await profile.get_clan()
	    em = discord.Embed(color=discord.Color.gold())
        em.title = profile.name
        em.description = f'{tag}\'s info'
        em.add_field(name='Favourite card:', value=profile.stats.favorite_card.name)
        em.add_field(name='chests', value=profile.chests.upcoming)
        em.add_field(name='clan name', value=clan.name)
        em.add_field(name='clan tag', value=clan.tag)
        em.add_field(name='clan type', value=clan.type)
        em.add_field(name='clan donations', value=clan.donations)
        em.add_field(name='clan members', value=clan.memberCount)
        await ctx.send(embed=em)
		
def setup(bot):
    bot.add_cog(Clash_Royale(bot))