import discord
from discord.ext import commands
from ext.paginator import Paginator
from motor import motor_asyncio
import os
import requests
import json
from ext import utils

class Fortnite:
    '''Get your fortnite stats here!!!'''
    def __init__(self, bot):
        self.bot = bot
        self.dbclient = motor_asyncio.AsyncIOMotorClient('mongodb://PikaBot:' + os.environ.get('DBPASS') + '@ds163711.mlab.com:63711/pikabot')
        self.db = self.dbclient.pikabot

    async def save_info(self, platform, username, authorID):
        await self.db.fortnite.update_one({'_id': authorID}, {'$set': {'_id': authorID, authorID: {"username": username, "platform": platform}}}, upsert=True)

    async def get_info(self, authorID):
        result = await self.db.fortnite.find_one({'_id': str(authorID)})
        if not result:
            return 'None'
        return (result[authorID]['platform'], result[authorID]['username'])

    def req(self, platform, username):
        headers: {
            "TRN-Api-Key": os.environ.get('FNTOKEN')
        }
        r = requests.get(f'https://api.fortnitetracker.com/v1/profile/{platform}/{username}', headers=headers)
        return r.json()

    def emoji(self, emoji):
        if emoji == 'chestmagic':
            emoji = 'chestmagical'
        with open('data/emojis.json') as f:
            emojis = json.load(f)
            e = emojis[emoji]
        return self.bot.get_emoji(e)

    @commands.command()
    async def fnsave(self, ctx, platform=None, username=None):
        '''Save your Fortnite stats here'''
        authorID = str(ctx.author.id)
        if not platform or not username:
            return await ctx.send(f'Please provide a a platform as well as a username `Usage: fnsave platform username`')
        try:
            await self.save_info(platform, username, authorID)
            await ctx.send(f'Your Platform `{platform}` and Username `{username}` have been successfully saved')
        except Exception as e:
            em = discord.Embed(color=utils.random_color())
            em.title = 'Error'
            em.description = str(e)
            await ctx.send(embed=em)


    @commands.command()
    async def fnprofile(self, ctx, platform=None, username=None):
        '''Gets your Fortnite Profile using Tag'''
        authorID = str(ctx.author.id)
        if not platform or not username:
            if await self.get_info(authorID) == 'None':
                await ctx.send(f'Please provide a tag or save your tag using `{ctx.prefix}fnsave platform username`')
            data = await self.get_info(authorID)
            platform = data[0]
            username = data[1]

        embeds = []
        data = self.req(platform, username)

        em = discord.Embed(color=utils.random_color())
        em.title = data['epicUserHandle']
        em.description = f'Overall Statistics'
        em.add_field(name='Platform', value=data['platformNameLong'])
        em.add_field(name=data['lifeTimeStats'][7]['key'], value=data['lifeTimeStats'][7]['value'])
        em.add_field(name=data['lifeTimeStats'][8]['key'], value=data['lifeTimeStats'][8]['value'])
        em.add_field(name=data['lifeTimeStats'][10]['key'], value=data['lifeTimeStats'][10]['value'])
        em.add_field(name=data['lifeTimeStats'][11]['key'], value=data['lifeTimeStats'][11]['value'])
        em.add_field(name=data['lifeTimeStats'][6]['key'], value=data['lifeTimeStats'][6]['value'])
        em.add_field(name=data['lifeTimeStats'][1]['key'], value=data['lifeTimeStats'][1]['value'])
        embeds.append(em)

        em = discord.Embed(color=utils.random_color())
        em.title = data['epicUserHandle']
        em.description = f'Solo Statistics'
        em.add_field(name='Matches played', value=data['stats']['p2']['matches']['value'])
        em.add_field(name='Wins', value=data['stats']['p2']['top1']['value'])
        em.add_field(name='Win %', value=data['stats']['p2']['winRatio']['value'])
        em.add_field(name='Score', value=data['stats']['p2']['Score']['value'])
        em.add_field(name='Kill/Deatch ratio', value=data['stats']['p2']['kd']['value'])
        em.add_field(name='kills', value=data['stats']['p2']['kills']['value'])
        em.add_field(name='Top 10', value=data['stats']['p2']['top10']['value'])
        em.add_field(name='Top 5', value=data['stats']['p2']['top5']['value'])
        embeds.append(em)

        em = discord.Embed(color=utils.random_color())
        em.title = data['epicUserHandle']
        em.description = f'Duo Statistics'
        em.add_field(name='Matches played', value=data['stats']['p10']['matches']['value'])
        em.add_field(name='Wins', value=data['stats']['p10']['top1']['value'])
        em.add_field(name='Win %', value=data['stats']['p10']['winRatio']['value'])
        em.add_field(name='Score', value=data['stats']['p10']['Score']['value'])
        em.add_field(name='Kill/Deatch ratio', value=data['stats']['p10']['kd']['value'])
        em.add_field(name='kills', value=data['stats']['p10']['kills']['value'])
        em.add_field(name='Top 10', value=data['stats']['p10']['top10']['value'])
        em.add_field(name='Top 5', value=data['stats']['p10']['top5']['value'])
        embeds.append(em)
        
        em = discord.Embed(color=utils.random_color())
        em.title = data['epicUserHandle']
        em.description = f'Squad Statistics'
        em.add_field(name='Matches played', value=data['stats']['p9']['matches']['value'])
        em.add_field(name='Wins', value=data['stats']['p9']['top1']['value'])
        em.add_field(name='Win %', value=data['stats']['p9']['winRatio']['value'])
        em.add_field(name='Score', value=data['stats']['p9']['Score']['value'])
        em.add_field(name='Kill/Deatch ratio', value=data['stats']['p9']['kd']['value'])
        em.add_field(name='kills', value=data['stats']['p9']['kills']['value'])
        em.add_field(name='Top 10', value=data['stats']['p9']['top10']['value'])
        em.add_field(name='Top 5', value=data['stats']['p9']['top5']['value'])
        embeds.append(em)

        p_session = Paginator(ctx, footer=f'PikaBot | info provided by TrackerNetwork (Kiling bugs one by one)', pages=embeds)
        await p_session.run()

def setup(bot):
    bot.add_cog(Fortnite(bot))