import discord
from discord.ext import commands

class info:
    '''Info related commands!'''
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.guild_only()
    async def info(self, ctx, user: discord.Member=None):
        """user info"""
        if not user:
            user = ctx.author
        embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what i found.", color=0x00ff00)
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Highest role", value=user.top_role)
        embed.add_field(name="Joined", value=user.joined_at)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)
     
    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx): 
        """server info"""
        embed = discord.Embed(name="{}'s info".format(ctx.message.guild.name), description="Here's what I could find.", color=0x00ff00)
        embed.set_author(name="Pika Bot")
        embed.add_field(name="Name", value=ctx.message.guild.name, inline=True)
        embed.add_field(name="ID", value=ctx.message.guild.id, inline=True)
        embed.add_field(name="Roles", value=len(ctx.message.guild.roles), inline=True)
        embed.add_field(name="Members", value=len(ctx.message.guild.members))
        embed.set_thumbnail(url=ctx.message.guild.icon_url)
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, user: discord.Member=None):
        """an avatar picture"""
        member = member or ctx.author
        av = member.avatar_url
        embed = discord.Embed(name="{}'s avatar!".format(ctx.message.guild.name), color=0x00ff00)
        embed.set_author(name="Pika Bot")
        embed.set_image(url=av)
        await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(info(bot))
