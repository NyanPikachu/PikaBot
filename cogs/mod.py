import discord
from discord.ext import commands

class mod:
    '''Moderation commands!'''
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx ,user: discord.Member=None, *, reason: str):
        '''Kick a member from the server!'''
        if not user:
            await ctx.send("Please mention a member for this command to work")
        try:
            embed = discord.Embed(title="Kick".format(user.name), description=f"{ctx.guild.name}", color=0xff0000)
            embed.add_field(name=f"{ctx.author} has kicked {user.name}", value=reason) 
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.guild.kick(user)
        except discord.Forbidden:
            await ctx.send("I could not kick the member, Please check i have your permissions")
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx ,user: discord.Member=None, *, reason: str):
        '''Ban a member from the server!'''
        if not user:
            await ctx.send("Please mention a member for this command to work")
        try:
            embed = discord.Embed(title="Ban".format(user.name), description=f"{ctx.guild.name}", color=0xff0000)
            embed.add_field(name=f"{ctx.author} has banned {user.name}", value=reason) 
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.guild.ban(user)
        except discord.Forbidden:
            await ctx.send("I could not ban the member, Please check your permissions")
    
def setup(bot):
    bot.add_cog(mod(bot))
