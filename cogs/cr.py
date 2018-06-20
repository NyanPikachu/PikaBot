import discord
import clashroyale
import os
import json
from motor import motor_asyncio
from ext import utils
from discord.ext import commands
from ext.paginator import Paginator

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
    def get_chests(self, ctx, cycle):
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
        p_battles = await self.client.get_player_battles(tag)
        cycle = await self.client.get_player_chests(tag)
        chests = self.get_chests(ctx, cycle)[0]
        special = self.get_chests(ctx, cycle)[1]

        hasClan = True
        try:
            clan = await profile.get_clan()
        except Exception as e:
            hasClan = False

        embeds = []

        em = discord.Embed(color=utils.random_color())
        em.title = profile.name
        em.description = f'{tag}\'s info'
        em.add_field(name=f'Trophies {self.emoji('trophy')}', value=profile.trophies)
        em.add_field(name=f'Max Trophies {self.emoji('trophy')}', value=profile.stats.maxTrophies)
        em.add_field(name=f'Arena', value=profile.arena.name)
        em.add_field(name=f'League', value=profile.arena.arena)
        em.add_field(name=f'Rank', value=profile.rank)
        em.add_field(name=f'games played', value=profile.games.total)
        em.add_field(name=f'Wins', value=profile.games.wins)
        em.add_field(name=f'Wins', value=profile.games.wins)
        em.add_field(name=f'Losses', value=profile.games.losses)
        em.add_field(name=f'Draws', value=profile.games.draws)
        em.add_field(name=f'Cards Found', value=profile.stats.cardsFound)
        em.add_field(name=f'Favourite card:', value=profile.stats.favorite_card.name)
        em.add_field(name=f'Upcoming Chests:', value=chests, inline=False)
        em.add_field(name=f'Chests Until:', value=special, inline=False)
        embeds.append(em)

        em = discord.Embed(color=utils.random_color())
        em.title = profile.name
        em.description = f'{tag}\'s Deck'
        em.add_field(name=profile.current_deck[0].name, value=f'**Rarity:** {profile.current_deck[0].rarity}\n**Elixir:** {profile.current_deck[0].elixir}\n**Level:** {profile.current_deck[0].level}\n**Description:** {profile.current_deck[0].description}')
        em.add_field(name=profile.current_deck[1].name, value=f'**Rarity:** {profile.current_deck[1].rarity}\n**Elixir:** {profile.current_deck[1].elixir}\n**Level:** {profile.current_deck[1].level}\n**Description:** {profile.current_deck[1].description}')
        em.add_field(name=profile.current_deck[2].name, value=f'**Rarity:** {profile.current_deck[2].rarity}\n**Elixir:** {profile.current_deck[2].elixir}\n**Level:** {profile.current_deck[2].level}\n**Description:** {profile.current_deck[2].description}')
        em.add_field(name=profile.current_deck[3].name, value=f'**Rarity:** {profile.current_deck[3].rarity}\n**Elixir:** {profile.current_deck[3].elixir}\n**Level:** {profile.current_deck[3].level}\n**Description:** {profile.current_deck[3].description}')
        em.add_field(name=profile.current_deck[4].name, value=f'**Rarity:** {profile.current_deck[4].rarity}\n**Elixir:** {profile.current_deck[4].elixir}\n**Level:** {profile.current_deck[4].level}\n**Description:** {profile.current_deck[4].description}')
        em.add_field(name=profile.current_deck[5].name, value=f'**Rarity:** {profile.current_deck[5].rarity}\n**Elixir:** {profile.current_deck[5].elixir}\n**Level:** {profile.current_deck[5].level}\n**Description:** {profile.current_deck[5].description}')
        em.add_field(name=profile.current_deck[6].name, value=f'**Rarity:** {profile.current_deck[6].rarity}\n**Elixir:** {profile.current_deck[6].elixir}\n**Level:** {profile.current_deck[6].level}\n**Description:** {profile.current_deck[6].description}')
        em.add_field(name=profile.current_deck[7].name, value=f'**Rarity:** {profile.current_deck[7].rarity}\n**Elixir:** {profile.current_deck[7].elixir}\n**Level:** {profile.current_deck[7].level}\n**Description:** {profile.current_deck[7].description}')
        embeds.append(em)

        if hasClan:
            em = discord.Embed(color=utils.random_color())
            em.title = profile.name
            em.description = 'You can use the clan command for more information on this clan!'
            em.set_image(url=clan.badge.image)
            em.add_field(name='Name', value=clan.name)
            em.add_field(name='Tag', value=clan.tag)
            em.add_field(name='Type', value=clan.type)
            em.add_field(name='Role', value=clan.role or 'Member')
            em.add_field(name='Donations', value=clan.donations)
            em.add_field(name='Members', value=clan.memberCount)
            embeds.append(em)
        else:
            clans = await self.client.get_top_clans()
            em = discord.Embed(color=utils.random_color())
            em.title = profile.name
            em.description = 'huh, looks like you are not in a clan yet! Joining a clan gives you extra fancy features ya know? like Clan Wars and cards donation(yup those donation that you saw on the previous screen, if you ever notice that). These are some of the top clans right now!'
            em.add_field(name='Top Clans #1:', value=clans[0]['name'])
            em.add_field(name='Top Clans #2:', value=clans[1]['name'])
            em.add_field(name='Top Clans #3:', value=clans[2]['name'])
            em.add_field(name='Top Clans #4:', value=clans[3]['name'])
            embeds.append(em)

        p_session = Paginator(ctx, footer=f'PikaBot | Created by Nyan Pikachu#4148 (does anybody read these?)', pages=embeds)
        await p_session.run()

    @commands.command()
    async def crclan(self, ctx, tag: str=None):
        authorID = str(ctx.author.id)
        if not tag:
            if await self.get_tag(authorID) == 'None':
                await ctx.send(f'Please provide a tag or save your tag using `{ctx.prefix}crsave <tag>`')
            tag = await self.get_tag(authorID)
            profile = await self.client.get_player(tag)
            try:
                clan = await profile.get_clan()
            except Exception:
                await ctx.send('Welp! if you ran this command without a tag then you are not in a clan right now!')
        else:
            try:
                clan = await self.client.get_clan(tag)
            except Exception:
                await ctx.send('Looks like there was an error! Please check your clan tag, if you are :100: sure this is not a typo contact me')

        em = discord.Embed(color=utils.random_color())
        em.title = 'Clan Info!'
        em.add_field(name='Name', value=clan.name)
        em.add_field(name='Tag', value=clan.tag)
        em.add_field(name='Type', value=clan.type)
        em.add_field(name='Role', value=clan.role or 'Member')
        em.add_field(name='Donations', value=clan.donations)
        em.add_field(name='Members', value=clan.memberCount)
        em.set_footer(text='PikaBot | Created by Nyan Pikachu#4148 (Notice me Senpai!)')
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Clash_Royale(bot))
