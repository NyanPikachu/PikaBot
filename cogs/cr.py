import discord
from discord.ext import commands
from ext.paginator import Paginator
import clashroyale
import os
import json
from motor import motor_asyncio

class Clash_Royale:
    '''Clash Royale commands to get your fancy stats here!'''
    def __init__(self, bot):
        self.bot = bot
        self.token = (os.environ.get('CRTOKEN'))
        self.client = clashroyale.Client(self.token, is_async=True)
        self.dbclient = motor_asyncio.AsyncIOMotorClient('mongodb://PikaBot:' + os.environ.get('DBPASS') + '@ds163711.mlab.com:63711/pikabot')
        self.db = self.dbclient.pikabot

    def check_tag(self, tag):
        for char in tag:
            if char.upper() not in '0289PYLQGRJCUV':
                return False
        return True

    async def save_tag(self, tag, authorID):
        await self.db.clashroyale.update_one({'_id': authorID}, {'$set': {'_id': authorID, 'tag': tag}}, upsert=True)

    async def get_tag(self, authorID):
        result = await self.db.clashroyale.find_one({'_id': authorID})
        if not result:
            return 'None'
        return result['tag']

    def emoji(self, emoji):
        if emoji == 'chestmagic':
            emoji = 'chestmagical'
        with open('data/emojis.json') as f:
            emojis = json.load(f)
            e = emojis[emoji]
        return self.bot.get_emoji(e)

    #next lines of codes are provided by RemixBot, we give full credits to them
    def get_chests(self, ctx, profile):
        cycle = profile.chest_cycle
        chests = f'| {self.emoji("chest" + cycle.upcoming[0].lower())} | '
        chests += ''.join([f'{self.emoji("chest" + cycle.upcoming[x].lower())}' for x in range(1, 8)])
        special = f'{self.emoji("chestsupermagical")}{cycle.super_magical} {self.emoji("chestmagical")}{cycle.magical} {self.emoji("chestlegendary")}{cycle.legendary} {self.emoji("chestepic")}{cycle.epic} {self.emoji("chestgiant")}{cycle.giant}'
        return (chests, special)

    @commands.command()
    async def crsave(self, ctx, tag=None):
        """Save Clash Royale your tag"""
        #crdb = self.getcoll("clashroyale")
        authorID = str(ctx.author.id)
        if not tag:
            return await ctx.send(f'Please provide a tag `Usage: crsave tag`')
        tag = tag.strip('#').replace('O', '0')
        if not self.check_tag:
            return await ctx.send('Invalid Tag. Please make sure your tag is correct then try again')
        await self.save_tag(tag, authorID)
        await ctx.send(f'Your tag `#{tag}` has been successfully saved')

    @commands.command()
    async def crprofile(self, ctx, tag: str=None):
        '''Gets your Clash Royale Profile using Tag'''
        authorID = str(ctx.author.id)
        if not tag:
            if await self.get_tag(authorID) == 'None':
                await ctx.send(f'Please provide a tag or save your tag using `{ctx.prefix}crsave <tag>`')
            tag = await self.get_tag(authorID)
        profile = await self.client.get_player(tag)

        chests = self.get_chests(ctx, profile)[0]
        special = self.get_chests(ctx, profile)[1]

        hasClan = True
        try:
            clan = await profile.get_clan()
        except Exception as e:
            hasClan = False

        embeds = []

        em = discord.Embed(color=discord.Color.gold())
        em.title = profile.name
        em.description = f'{tag}\'s info'
        em.add_field(name='Trophies', value=profile.trophies)
        em.add_field(name='Max Trophies', value=profile.stats.maxTrophies)
        em.add_field(name='Arena', value=profile.arena.name)
        em.add_field(name='League', value=profile.arena.arena)
        em.add_field(name='Rank', value=profile.rank)
        em.add_field(name='Wins', value=profile.games.wins)
        em.add_field(name='Wins', value=profile.games.wins)
        em.add_field(name='Losses', value=profile.games.losses)
        em.add_field(name='Draws', value=profile.games.draws)
        em.add_field(name='Cards Found', value=profile.stats.cardsFound)
        em.add_field(name='Favourite card:', value=profile.stats.favorite_card.name)
        em.add_field(name='Upcoming Chests:', value=chests, inline=False)
        em.add_field(name='Chests Until:', value=special, inline=False)
        em.set_footer(text=f'Bot made by Nyan Pikachu#4148 | Wrapper provided by CodeGrok, API by RoyaleAPI')
        embeds.append(em)

        if hasClan:
            em = discord.Embed(color=discord.Color.gold())
            em.title = profile.name
            em.add_field(name='Name', value=clan.name)
            em.add_field(name='Role', value=clan.role or 'Member')
            em.add_field(name='Tag', value=clan.tag)
            em.add_field(name='Type', value=clan.type)
            em.add_field(name='Donations', value=clan.donations)
            em.add_field(name='Members', value=clan.memberCount)
            em.set_footer(text=f'Bot made by Nyan Pikachu#4148 | Wrapper provided by CodeGrok, API by RoyaleAPI')
            embeds.append(em)

        message = ctx
        base = await ctx.send(content=None, embed=embeds[0])
        p_session = Paginator(message, base , embeds, self)
        await p_session.run()

def setup(bot):
    bot.add_cog(Clash_Royale(bot))
