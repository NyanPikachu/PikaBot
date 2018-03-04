import discord
from discord.ext import commands
from ext.paginator import PaginatorSession
import aiohttp

class Clash_Royale:
    '''Clash Royale commands to get your fancy stats here!'''
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def crprofile(tag: str=None):
        '''Gets your Clash Royale Profile using Tag!'''
        if not tag:
            return await ctx.send('Please provide a tag for this command to work `Usage : $crprofile [tag]`')
        headers = {"auth":"c94d84443b5345d784418332e81a5d3b272f67619a6b45368f2cbe5f064d3d55"}
        async with aiohttp.ClientSession as session:
            async with session.get("https://api.cr-api.com/players/{tag}", headers=headers) as resp:
                data = await resp.json()
        embed = discord.Embed(name=ctx.author.name)
        embed.add_field(name='Name', value=data['name'])
        await ctx.send(embed=embed)
        asyncio.get_event_loop().run_until_complete(main())
        
def setup(bot):
    bot.add_cog(Clash_Royale(bot))
