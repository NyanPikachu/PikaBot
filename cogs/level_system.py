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
        await self.db.xp.update_one({'_id': guildID}, {'$set': {'_id': guildID, userID: xp}}, upsert=True)

    async def on_message(self, message):
    	ch = message.channel
    	guild = message.guild.id
    	user = message.author.id

    	if message.author.bot:
    		return
    	try:
    		await self.update_xp(15, guild, user)
    	except Exception as e:
    		await ch.send(e)

    	await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(xp(bot))