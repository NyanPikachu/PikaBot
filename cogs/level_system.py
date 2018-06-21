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
    async def update_xp(self, userID, xp: int):
        await self.db.profiles.update_one({'_id': userID}, {'$set': {'_id': userID, userID: {"xp_amount": xp}}}, upsert=True)

    async def update_desc(self, userID, description):
        await self.db.profiles.update_one({'_id': userID}, {'$set': {'_id': userID, userID: {"description": description}}}, upsert=True)

    async def get_xp(self, userID):   
        try:
            result = await self.db.profiles.find_one({'_id': str(userID)})
            return result[userID]['xp_amount']
        except Exception:
            return 0

    async def get_desc(self, userID):
        try:
            result = await self.db.profiles.find_one({'_id': str(userID)})
            description = result[userID]['description']
            if description == None:
                await self.db.profiles.update_one({'_id': userID}, {'$set': {'_id': userID, userID: {'description': "I'm a very average person"}}})
            return description
        except Exception as e:
            print(str(e))

    #events
    async def on_member_join(self, member):
        userID = str(member.id)
        result = await self.db.profiles.find_one({'_id': str(userID)})
        description = result[userID]['description']
        if description != "I'm a very average person":
            pass
        elif not result or description:
            await self.db.profiles.update_one({'_id': userID}, {'$set': {'_id': userID, userID: {'description': "I'm a very average person"}}})


    async def on_message(self, message):
        if message.author.bot:
            return
        ch = message.channel
        guildID = str(message.guild.id)
        userID = str(message.author.id)
        try:
            old_xp = await self.get_xp(userID)
        except Exception:
            old_xp = 0
        new_xp =  int(old_xp) + 8
        try:
            await self.update_xp(userID, new_xp)
        except Exception as e:
            await ch.send(e)

    @commands.command()
    async def profile(self, ctx, user: discord.Member=None):
        if not user:
            user = ctx.author
        userID = str(user.id)
        guildID = str(ctx.guild.id)
        
        total_xp = await self.get_xp(userID)
        description = await self.get_desc(userID)

        embed = discord.Embed(color=utils.random_color())
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name='Total_XP', value=total_xp, inline=True)
        embed.add_field(name='Description', value=description, inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def description(self, ctx, body):
        userID = str(ctx.author.id)
        if len(body) >= 256:
            await ctx.send('Desciption must not be longer than 256 characters')
        else:
            try:
                self.update_desc(body)
                await ctx.send('Description updated :white_check_mark:')
            except Exception as e:
                em = discord.Embed(color=utils.random_color())
                em.description = str(e)
                await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(xp(bot))