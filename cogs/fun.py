import discord
from discord.ext import commands
import random
from random import randint
from pokedex import pokedex
import requests
from ext import utils
import os

class Fun:
    '''Miscellaneous commands that are fun!'''
    def __init__(self, bot):
        self.bot = bot
        self.pokedex = pokedex.Pokedex()
        self.gif_api_key = os.environ.get('GIFTOKEN')

    @commands.command()
    async def gif(self, ctx, *,search=None):
        """get a Gif by name"""
        if not search:
            em = discord.Embed(color=utils.random_color())
            em.title = f'Usage: {ctx.prefix}gif <search tag>'
            em.description ='Browse the Giphy website for Gifs'
            return await ctx.send(embed=em)
        try:
            r = requests.get(f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={self.gif_api_key}')
            data = r.json()
            await ctx.send(data['data'][0]['images']['fixed_height']['url'])
        except Exception as e:
            await ctx.send(f'Error : `{e}`')

    @commands.command()
    async def pokemon(self, ctx, poke: str=None):
        '''Get A Pokemon's info!'''
        pokemon = self.pokedex.get_pokemon_by_name(poke)
        try:
            em = discord.Embed(name=pokemon[0]['name'] + "'s info!", color=utils.random_color())
            em.set_author(name=pokemon[0]['name'] + "'s info!")
            em.add_field(name='Species', value=pokemon[0]['species'])
            em.add_field(name='Number', value=pokemon[0]['number'])
            em.add_field(name='Types', value=", ".join(pokemon[0]['types']))
            em.add_field(name=' Normal Abilities', value=", ".join(pokemon[0]['abilities']['normal']))
            em.add_field(name='Hidden Abilities', value=", ".join(pokemon[0]['abilities']['hidden']))
            em.add_field(name='Height', value=pokemon[0]['height'])
            em.add_field(name='Weight', value=pokemon[0]['weight'])
            em.add_field(name='Evolutions', value=", ".join(pokemon[0]['family']['evolutionLine']))
            em.set_thumbnail(url=pokemon[0]['sprite'])
            em.set_footer(text="Pika Bot | scripted in discord.py")
            await ctx.send(embed=em)
        except Exception:
            await ctx.send('Could not find that Pokemon. Please check your pokemon\'s name')
    
    @commands.command()
    async def hug(self, ctx, user: discord.Member=None):
        """hugs a user"""
        if not user:
            em = discord.Embed(color=utils.random_color())
            em.title = f'Usage: {ctx.prefix}hug <user>'
            em.description ='Hug a person with a random Gif!'
            return await ctx.send(embed=em)
        r = requests.get(f'http://api.giphy.com/v1/gifs/random?tag=hug&api_key={self.gif_api_key}')
        data = r.json()
        embed = discord.Embed(title="Hug!".format(user.name), description= f"{ctx.author} has sent {user} a hug !", color=utils.random_color())
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_image(url=data['data']['images']['fixed_height']['url'])
        await ctx.send(embed=embed)
        
    @commands.command(hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, msg: str):
        """owner only command- print a message"""
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def embedsay(self, ctx, *, body: str):
        '''Send a simple embed'''
        em = discord.Embed(description=body)
        await ctx.send(embed=em)
    
    @commands.command()
    async def coinflip(self, ctx):
        """Flips a coin!"""
        flip = random.choice(["Heads", "Tails"])
        await ctx.send(flip)

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, magic=None):
        if not magis:
            em = discord.Embed(color=utils.random_color())
            em.title = f'Usage: {ctx.prefix}8ball <Yes/No question>'
            em.description ='Ask the Mighty 8Ball a question!'
            return await ctx.send(embed=em)
        responses = [
        "Yes, Of course",
        "Definitely",
        "Sure",
        "Maybe",
        "Never",
        "No, Just no",
        "Definitely....no",
        "I will tell you later",
        "Ask me again"
        ]

        em = discord.Embed(color=utils.random_color())
        em.title = "8Ball"
        em.add_field(name="Question:", value=magic)
        em.add_field(name='Respone:', value=random.choice(responses))
        await ctx.send(embed=em)
    
def setup(bot):
    bot.add_cog(Fun(bot))