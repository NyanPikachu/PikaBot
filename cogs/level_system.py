import discord
from discord.ext import commands
from motor import motor_asyncio
from ext import utils

class xp:
    '''XP commands for leveling System within the bot'''
    def __init__(self, bot):
        self.bot = bot
        self.dbclient = motor_asyncio.AsyncIOMotorClient('mongodb://PikaBot:' + os.environ.get('DBPASS') + '@ds163711.mlab.com:63711/pikabot')
        self.db = self.dbclient.pikabot

    async def update_xp(self, xp: int, guildID, userID):
        await self.db.xp.update_one({'_id': userID}, {'$set': {'_id': guildID: {userID: xp}}}, upsert=True)

    async def get_xp(self, guildID, userID):
    	try:
    		result = await db.settings.find_one({'_id': userID})
    	except Exception as e:
    		er = f'error : `{e}`'
    		return er


    @self.bot.event
    async def on_message(message):
    	ch = message.channel
    	guild = message.guild.id
    	user = message.author.id

    	if message.author.bot:
    		return
    	try:
    		update_xp(15, guild, user)
    	except Exception as e:
    		await ch.send(e)

    	await bot.process_commands(message)

def setup(bot):
    bot.add_cog(xp(bot))