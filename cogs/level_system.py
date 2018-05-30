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

    async def update_xp(self, xp: int, guildID, userID):
        await self.db.xp.update_one({'_id': guildID}, {'$set': {'_id': guildID, userID: {"xp_amount": xp}}}, upsert=True)

    async def get_xp(self, guildID, userID):   
        result = await self.db.xp.find_one({'_id': guildID})
        return result['userID']['xp_amount']
        if not result or not result.get('userID')('xpamount'):
            return 0

    async def on_message(self, message):
        ch = message.channel
        guild = str(message.guild.id)
        user = str(message.author.id)
        try:
            old_xp = await self.get_xp(guild, user)
        except Exception:
            old_xp = 0
        new_xp =  int(old_xp) + 15

        if message.author.bot:
            return
        try:
            await self.update_xp(new_xp, guild, user)
        except Exception as e:
            await ch.send(e)

        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(xp(bot))