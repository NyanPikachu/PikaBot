import discord
from discord.ext import commands
from ext.paginator import PaginatorSession
import clashroyale
import os

class Clash_Royale:
    '''Clash Royale commands to get your fancy stats here!'''
    def __init__(self, bot):
        self.bot = bot
     
    token = os.environ.get("CRTOKEN")
        
    
    @commands.command()
    async def crprofile(self, ctx, tag: str=None):
        '''Gets your Clash Royale Profile using Tag!'''
        if not tag:
            return await ctx.send('Please provide a tag for this command to work `Usage : $crprofile [tag]`. saving tags will be implemented soon')
        client = clashroyale.Client(token, is_async=True) # is_async=True argument
        profile = await client.get_player(tag)
        clan = await profile.get_clan()
        em = discord.Embed(color=discord.Color.gold())
        em.title = profile.name
        em.description = f'{tag}\'s info'
        em.add_field(name='League Statistics:', value=profile.league_statistics)
        await profile.refresh()
        em.add_field(name='Favourite card:', value=profile.stats.favorite_card.name)
        em.add_field(name='Clan:', value=clan)
        em.add_field(name='Clan chest:', value=clan.clan_chest)
        await clan.refresh()
        client.close()
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Clash_Royale(bot))