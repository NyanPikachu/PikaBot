import discord
from discord.ext import commands
from ext.paginator import PaginatorSession
import requests

class Clash_Royale:
    '''Clash Royale commands to get your fancy stats here!'''
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def crprofile(self, ctx, tag: str=None):
        '''Gets your Clash Royale Profile using Tag!'''
        if not tag:
            return await ctx.send('Please provide a tag for this command to work `Usage : $crprofile [tag]`')
        headers = {
        	"auth": "c94d84443b5345d784418332e81a5d3b272f67619a6b45368f2cbe5f064d3d55"
       	}
        r = requests.get(f"https://api.cr-api.com/players/{tag}", headers=headers)
        cr = r.json()
        embed = discord.Embed(name=ctx.author.name)
        embed.add_field(name='Name', value=cr['name'])
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Clash_Royale(bot))
