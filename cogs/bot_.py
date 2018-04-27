import discord
from discord.ext import commands
from ext.paginator import Paginator
from ext import utils
import os
from motor import motor_asyncio

class Bot:
    '''Info related commands!'''
    def __init__(self, bot):
        self.bot = bot
        self.dbclient = motor_asyncio.AsyncIOMotorClient('mongodb://PikaBot:' + os.environ.get('DBPASS') + '@ds163711.mlab.com:63711/pikabot')
        self.db = self.dbclient.pikabot
    
    async def save_prefix(self, prefix, guildID):
        await self.db.settings.update_one({'_id': guildID}, {'$set': {'_id': guildID, 'prefix': prefix}}, upsert=True)

    @commands.command(name="bot")
    async def _bot(self, ctx):
        """Info about the bot"""
        embed = discord.Embed(color=utils.random_color())
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

    @commands.command()
    async def suggest(self, ctx, suggestion):
        """suggest a feature to be added!"""
        if not suggestion:
            em = discord.Embed(color=utils.random_color())
            em.title = f'Usage: {ctx.prefix}suggest <suggestion>'
            em.description ='suggest a feature to be added!'
            await ctx.send(embed=em)
        ch = self.bot.get_channel(439454261466628096)
        em = discord.Embed(color=utils.random_color())
        em.description = str(suggestion)
        em.title = 'Suggestion'
        em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ch.send(embed=em)
        await ctx.send('Thanks for your suggestion')

    @commands.command()
    async def invite(self, ctx):
        """Get an invite link of the bot"""
        await ctx.send(f'Invite me to your server using this link: \nhttps://discordapp.com/api/oauth2/authorize?client_id={bot.use.id}&permissions=0&scope=bot')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def prefix(self, ctx, prefix=None):
        """Change Prefix of the server"""
        guildID = str(ctx.guild.id)
        if not prefix:
            em = discord.Embed(color=utils.random_color())
            em.title = f'Usage: {ctx.prefix}prefix <prefix>'
            em.description ='Pick a custom server prefix!'
            await ctx.send(embed=em)
        await self.save_prefix(prefix, guildID)
        await ctx.send(f'Prefix `{prefix}` successfully saved (re-run this command to replace it)')
        
def setup(bot):
    bot.add_cog(Bot(bot))