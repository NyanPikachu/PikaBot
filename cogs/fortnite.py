import discord
from discord.ext import commands
import pynite
from ext.paginator import PaginatorSession

class Fortnite:
    '''Get Fortnite stats by name'''

    def __init__(self, bot):
        self.bot = bot
       
        
    @commands.command()
    async def fnprofile(self, ctx, plat=None, *, name=None):
        '''Get stats for your fortnite account !'''
        if name is None:
            await ctx.send("Please specify a username as well as the platform (defaults to pc if not specified).")
            return

        if plat not in ['psn', 'xbl', 'pc']:
            await ctx.send("Invalid platform, platforms are {psn, xbl, pc}.")
            return

        pages = []
        client = pynite.Client('5a20baea-b8a7-4e42-9de3-741534219452')
        player = await client.get_player(plat, name)
        lifetime = await player.get_lifetime_stats()
        solo = await player.get_solos()
        duos = await player.get_duos()
        squads = await player.get_squads()
        
        embed = discord.Embed(color=discord.Color.blue())
        embed.title = 'Name: ' + player.epic_user_handle + ' - LifeTime stats'
        embed.description = 'Platform: ' + player.platform_name_long
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
        
        embed = discord.Embed(color=discord.Color.blue())
        embed.title = 'Name: ' + player.epic_user_handle + ' - Solo Stats'
        embed.description = 'Platform: ' + player.platform_name_long
        embed.add_field(name='Victory Royales', value=solo.top1.value)
        embed.add_field(name='Top 10', value=solo.top10.value)
        embed.add_field(name='Score', value=solo.score.value)
        embed.add_field(name='K/D', value=solo.kd.value)
        embed.add_field(name='Kills', value=solo.kills.value)
        embed.add_field(name='Average kills per match', value=solo.kpg.value)
        embed.add_field(name='Matches Played', value=solo.matches.value)
        
        pages.append(embed)
        
        embed = discord.Embed(color=discord.Color.blue())
        embed.title = 'Name: ' + player.epic_user_handle + ' - Duo Stats'
        embed.description = 'Platform: ' + player.platform_name_long
        embed.add_field(name='Victory Royales', value=solo.top1.value)
        embed.add_field(name='Top 10', value=duos.top10.value)
        embed.add_field(name='Score', value=duos.score.value)
        embed.add_field(name='K/D', value=duos.kd.value)
        embed.add_field(name='Kills', value=duos.kills.value)
        embed.add_field(name='Average kills per match', value=duos.kpg.value)
        embed.add_field(name='Matches Played', value=duos.matches.value)
        
        pages.append(embed)
        
        embed = discord.Embed(color=discord.Color.blue())
        embed.title = 'Name: ' + player.epic_user_handle + ' - Squad Stats'
        embed.description = 'Platform: ' + player.platform_name_long
        embed.add_field(name='Victory Royales', value=solo.top1.value)
        embed.add_field(name='Top 10', value=squads.top10.value)
        embed.add_field(name='Score', value=squads.score.value)
        embed.add_field(name='K/D', value=squads.kd.value)
        embed.add_field(name='Kills', value=squads.kills.value)
        embed.add_field(name='Average kills per match', value=squads.kpg.value)
        embed.add_field(name='Matches Played', value=squads.matches.value)
        
        pages.append(embed)
        p_session = PaginatorSession(ctx, footer=f'Bot made by Nyan Pikachu#4148 | Powered by fortnitetracker.com', pages=pages)
        await p_session.run()
        
def setup(bot):
    bot.add_cog(Fortnite(bot))