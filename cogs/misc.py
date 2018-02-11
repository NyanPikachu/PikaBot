import discord
from discord.ext import commands

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
    
def setup(bot):
    bot.add_cog(misc(bot))
