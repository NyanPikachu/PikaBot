import discord
from discord.ext import commands
from ext.paginator import PaginatorSession
import clashroyale
import os
import json

class Clash_Royale:
    '''Clash Royale commands to get your fancy stats here!'''
    def __init__(self, bot):
        self.bot = bot
        self.token = (os.environ.get('CRTOKEN'))
        self.client = clashroyale.Client(self.token, is_async=True)
        
    @commands.command()
    async def crprofile(self, ctx, tag: str=None):
        '''Gets your Clash Royale Profile using Tag!'''
        if not tag:
            return await ctx.send('Please provide a tag for this command')
        profile = await self.client.get_player(tag)
        hasClan = True
        try:
            clan = await profile.get_clan()
        except Exception as e:
            hasClan = False

        pages = []

        if hasProfile:
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
            em.title = clan.name
            em.thumbnail = clan.badge.image
            em.add_field(name='Name', value=clan.name)
            em.add_field(name='Role', value=clan.role)
            em.add_field(name='Tag', value=clan.tag)
            em.add_field(name='Type', value=clan.type)
            em.add_field(name='Donations', value=clan.donations)
            em.add_field(name='Members', value=clan.memberCount)
            pages.append(em)

        p_session = PaginatorSession(ctx, footer=f'Bot made by Nyan Pikachu#4148 | Wrapper provided by CodeGrok, API by RoyaleAPI', pages=pages)
        await p_session.run()

def setup(bot):
    bot.add_cog(Clash_Royale(bot))