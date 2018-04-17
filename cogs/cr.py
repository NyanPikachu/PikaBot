import discord
from discord.ext import commands
from ext.paginator import PaginatorSession
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
        self.mongoclient = motor_asyncio.AsyncIOMotorClient('mongodb://Nyan Pikachu:' + os.environ.get('DBPASS') + '@ds163711.mlab.com:63711/pikabot')

    async def get_tag(self, userid):
        result = await self.db.clashroyale.find_one({'_id': userid})
        if not result:
            return 'None'
        return result['tag']

    def check_tag(self, tag):
        for char in tag:
            if char.upper() not in '0289PYLQGRJCUV':
                return False
        return True

    def getcoll(self, game):
        return getattr(self.mongoclient, game)

    @commands.command()
    async def crsave(self, ctx, tag=None):
        crdb = self.getcoll("clashroyale")
        authorID = str(ctx.author.id)
        if not tag:
            return await ctx.send(f'Please provide a tag `Usage: crsave tag`')
        document = {authorID: tag}
        try:
            await crdb.insert_one(document)
        except Exception as e:
            await ctx.send(f'Error: `{str(e)}`')

    @commands.command()
    async def crprofile(self, ctx, tag: str=None):
        '''Gets your Clash Royale Profile using Tag!'''
                #following lines of code was taken from cree-py/remix-bot full credits to them
        if tag is None:
            if await self.get_tag(str(ctx.author.id)) == 'None':
                return await ctx.send(f'No tag found. Please use `{ctx.prefix}save <tag>` to save a tag to your discord profile.')
            tag = await self.get_tag(str(ctx.author.id))
            try:
                profile = await self.client.get_player(tag)
            except (clashroyale.errors.NotResponding, clashroyale.errors.ServerError) as e:
                return await ctx.send(f'`Error {e.code}: {e.error}`')
        else:
            if not self.check_tag(tag):
                return await ctx.send('Invalid Tag. Please make sure your tag is correct.')
            try:
                profile = await self.client.get_player(tag.strip('#').replace('O', '0'))
            except (clashroyale.errors.NotResponding, clashroyale.errors.ServerError) as e:
                return await ctx.send(f'`Error {e.code}: {e.error}`')
            except Exception as e:
                return await ctx.send('Please provide a tag for this command')

        profile = await self.client.get_player(tag)

        hasClan = True
        try:
            clan = await profile.get_clan()
        except Exception as e:
            hasClan = False

        pages = []

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
        pages.append(em)

        if hasClan:
            em = discord.Embed(color=discord.Color.gold())
            em.title = profile.name
            em.add_field(name='Name', value=clan.name)
            em.add_field(name='Role', value=clan.role or 'Member')
            em.add_field(name='Tag', value=clan.tag)
            em.add_field(name='Type', value=clan.type)
            em.add_field(name='Donations', value=clan.donations)
            em.add_field(name='Members', value=clan.memberCount)
            pages.append(em)

        p_session = PaginatorSession(ctx, footer=f'Bot made by Nyan Pikachu#4148 | Wrapper provided by CodeGrok, API by RoyaleAPI', pages=pages)
        await p_session.run()

def setup(bot):
    bot.add_cog(Clash_Royale(bot))