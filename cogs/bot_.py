import discord
from discord.ext import commands
from ext.paginator import Paginator
from ext import utils
import os

class info:
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

    @commands.command()
    async def suggest(self, ctx, suggestion):
        """suggest a feature to be added!"""
        if not suggestion:
            em = discord.Embed(color=utils.random_color)
            em.title = f'Usage: {ctx.prefix}suggest <suggestion>'
            em.description ='suggest a feature to be added!'
            await ctx.send(embed=em)
        ch = self.bot.get_channel(439454261466628096)
        em = discord.Embed(color=utils.random_color)
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
            await ctx.send('Please provide a prefix for this command to work')
        await self.save_prefix(prefix, guildID)
        await ctx.send(f'Prefix `{prefix}` successfully saved (re-run this command to replace it)')

    @commands.command(name='presence')
    @utils.developer()
    async def _presence(ctx, type: str=None, *, game: str=None):
        '''Change the bot's presence'''
        if type is None:
            await ctx.send(f'Usage: `{ctx.prefix}presence [game/stream/watch/listen] [message]`')
        else:
            if type.lower() == 'stream':
                await self.bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.streaming))
                await ctx.send(f'Set presence to. `Streaming {game}`')
            elif type.lower() == 'game':
                await self.bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.playing))
                await ctx.send(f'Set presence to `Playing {game}`')
            elif type.lower() == 'watch':
                await self.bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.watching))
                await ctx.send(f'Set presence to `Watching {game}`')
            elif type.lower() == 'listen':
                await self.bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.listening))
                await ctx.send(f'Set presence to `Listening to {game}`')
            elif type.lower() == 'clear':
                await self.bot.change_presence(activity=discord.Activity(name=None))
                await ctx.send('Cleared Presence')
            else:
                await ctx.send('Usage: `.presence [game/stream/watch/listen] [message]`')
        
def setup(bot):
    bot.add_cog(info(bot))