import discord
from discord.ext import commands
from motor import motor_asyncio
from ext import utils
import os

class xp:
    '''XP commands for leveling System within the bot'''
    def __init__(self, bot):
        self.bot = bot
        self.dbclient = motor_asyncio.AsyncIOMotorClient('mongodb://PikaBot:' + os.environ.get('DBPASS') + '@ds163711.mlab.com:63711/pikabot')
        self.db = self.dbclient.pikabot

    #functions
    async def update_xp(self, guildID, userID, xp: int):
        await self.db.xp.update_one({'_id': guildID}, {'$set': {'_id': guildID, userID: {"xp_amount": xp}}}, upsert=True)

    async def get_xp(self, guildID, userID):   
        try:
            result = await self.db.xp.find_one({'_id': str(guildID)})
            return result[userID]['xp_amount']
        except Exception:
            return 0

    async def get_desc(self, userID):
        try:
            result = await self.db.profiles.find_one({'_id': str(userID)})
            description = result[userID]['description']
        except Exception:
            await self.db.profiles.update_one({'_id': userID}, {'$set': {'_id': userID, userID: {'description': "I'm a very average person"}}})

    #events
    async def on_member_join(member):
        userID = str(member.id)
        try:
            result = await self.db.profiles.find_one({'_id': str(userID)})
            description = result[userID]['description']
            if description != "I'm a very average person":
                pass
            elif not result or description:
                await self.db.profiles.update_one({'_id': userID}, {'$set': {'_id': userID, userID: {'description': "I'm a very average person"}}})
        except Exception as e:
            err = f"Error: `{e}`"

    async def on_message(self, message):
        ch = message.channel
        guildID = str(message.guild.id)
        userID = str(message.author.id)
        try:
            old_xp = await self.get_xp(guildID, userID)
        except Exception:
            old_xp = 0
        new_xp =  int(old_xp) + 8

        if message.author.bot:
            return
        try:
            await self.update_xp(guildID, userID, new_xp)
        except Exception as e:
            await ch.send(e)

    @commands.command()
    async def profile(self, ctx, user: discord.Member=None):
        if not user:
            user = ctx.author
        userID = str(user.id)
        guildID = str(ctx.guild.id)
        
        total_xp = await self.get_xp(guildID, userID)

        embed = discord.Embed(color=utils.random_color())
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name='Description', value=self.get_desc)
        embed.add_field(name='Total_XP', value=total_xp)
        embed.set_thumbnail(url=user.avatar_url)

    @commands.command()
    async def description(self, ctx, body):
        userID = str(ctx.author.id)
        if len(body) >= 256:
            await ctx.send('Desciption must not be longer than 256 characters')
        else:
            await self.db.profiles.update_one({'_id': userID}, {'$set': {'_id': userID, userID: {'description': body}}})
            await ctx.send('Description updated :white_check_mark:')

def setup(bot):
    bot.add_cog(xp(bot))