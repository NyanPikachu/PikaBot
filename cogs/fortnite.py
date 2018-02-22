import discord
from discord.ext import commands
import pynite
from ext.paginator import PaginatorSession

class Fortnite:
    '''Get Fortnite stats by name'''

    def __init__(self, bot):
        self.bot = bot
       
        
    @commands.command()
    async def fnprofile(self, ctx, plat=None, name=None):
        pages = []
        client = pynite.Client('5a20baea-b8a7-4e42-9de3-741534219452')
        player = await client.get_player(plat, name)
        lifetime = await player.get_lifetime_stats()
        solo = await player.get_solos()
        
        embed = discord.Embed(color=discord.Color.green())
        embed.title = 'Name: ' + name
        embed.description = 'Platform: ' + plat
        embed.add_field(name=lifetime[9].key, value=lifetime[9].value)
        embed.add_field(name=lifetime[1].key, value=lifetime[1].value)
        embed.add_field(name=lifetime[4].key, value=lifetime[4].value)
        embed.add_field(name=lifetime[6].key, value=lifetime[6].value)
        embed.add_field(name=lifetime[7].key, value=lifetime[7].value)
        embed.add_field(name=lifetime[13].key, value=lifetime[13].value)
        embed.add_field(name=lifetime[10].key, value=lifetime[10].value)
        embed.add_field(name=lifetime[11].key, value=lifetime[11].value)
        embed.add_field(name=lifetime[12].key, value=lifetime[12].value)
        
        pages.append(embed)
        
        embed = discord.Embed(color=discord.Color.green())
        embed.title = 'Name: ' + name
        embed.description = 'Platform: ' + plat
        embed.add_field(name='Victory Royales', value=solo.top1.value)
        embed.add_field(name='Top 10', value=solo.top10.value)
        embed.add_field(name='Score', value=solo.score.value)
        embed.add_field(name='K/D', value=solo.kd.value)
        embed.add_field(name='Kills', value=solo.kills.value)
        embed.add_field(name='Matches Played', value=solo.matches.value)
        embed.add_field(name='Time Played', value=solo.minutes_played.value)
        
        pages.append(embed)
        
        p_session = PaginatorSession(ctx, footer=f'Stats made by Cree-Py | Powered by fortnitetracker.com', pages=pages)
        await p_session.run()
        
        
def setup(bot):
    bot.add_cog(Fortnite(bot))
