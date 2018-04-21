import discord
from discord.ext import commands
from ext.paginator import PaginatorSession
import os

class info:
    '''Info related commands!'''
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="bot")
    async def _bot(self, ctx):
        """Info about the bot"""
        embed = discord.Embed(color=0xf1c40f)
        embed.title = "Bot info"
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.author.avatar_url)
        embed.description = "A simple bot created by Nyan Pikachu#4148"
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Online Users", value=str(len({m.id for m in self.bot.get_all_members() if m.status is not discord.Status.offline})))
        embed.add_field(name="Total Users", value=len(self.bot.users))
        embed.add_field(name="Channels", value=f"{sum(1 for g in self.bot.guilds for _ in g.channels)}")
        embed.add_field(name="Latency", value=f"{self.bot.ws.latency * 100:.3f} ms")
        embed.add_field(name="Library", value="discord.py")
        embed.add_field(name="Source", value="[GitHub](https://github.com/NyanPikachu/PikaBot)")
        embed.set_footer(text="Pika Bot | scripted in discord.py")
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['ui'])
    @commands.guild_only()
    async def userinfo(self, ctx, user: discord.Member=None):
        """user info"""
        if not user:
            user = ctx.author
        embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what i found.", color=user.Role.colour)
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Game", value=str(user.activity))
        embed.add_field(name="Highest role", value=user.top_role.name or "Empty")
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
        embed.add_field(name="Owner", value=(ctx.message.guild.owner))
        embed.add_field(name="Created at", value=(ctx.message.guild.created_at))
        embed.set_thumbnail(url=ctx.message.guild.icon_url)
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, user: discord.Member=None):
        """an avatar picture"""
        if not user:
            user = ctx.author
        av = user.avatar_url
        embed = discord.Embed(name="{}'s avatar!".format(ctx.message.guild.name), color=0x0080ff)
        embed.set_author(name=f"{user.name}'s avatar!")
        embed.set_image(url=av)
        await ctx.send(embed=embed)
       
def setup(bot):
    bot.add_cog(info(bot))