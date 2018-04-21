import discord
from discord.ext import commands
import random
from random import randint
from pokedex import pokedex
import requests
import os
from spotify_api.api import SpotifyApi

class Fun:
    '''Miscellaneous commands that are fun!'''
    def __init__(self, bot):
        self.bot = bot
        self.pokedex = pokedex.Pokedex()
        self.gif_api_key = os.environ.get('GIFTOKEN')
        self.spotify = SpotifyApi()

    @commands.command()
    async def gif(self, ctx, *,search=None):
        """get a Gif by name"""
        if not search:
            await ctx.send('Please provide a search tag to run this command')
        search = search.replace(' ', '+')
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
            em = discord.Embed(name=pokemon[0]['name'] + "'s info!")
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
            await ctx.send(f"Please mention someone for this command to work {ctx.author.mention}" )
        r = requests.get(f'http://api.giphy.com/v1/gifs/random?tag=hug&api_key={self.gif_api_key}')
        data = r.json()
        embed = discord.Embed(title="Hug!".format(user.name), description= f"{ctx.author} has sent {user} a hug !", color=0xffb6c1)
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

    #spotify command group
    @commands.group(pass_context=True, invoke_without_command=True)
    async def spotify(self, ctx):
        '''Search for Spotify albums, tracks and artists'''

    @spotify.command(pass_context=True)
    async def album(self, ctx, search):
        results = api.albums.search(search)
        for album in results:
            await ctx.send(album)

    @spotify.command(pass_context=True)
    async def artist(self, ctx, search):
        results = api.artists.search(search)
        for artist in results:
            await ctx.send(artist)

    @spotify.command(pass_context=True)
    async def track(self, ctx, search):
        results = api.tracks.search(search)
        for track in results:
            await ctx.send(track)
    
def setup(bot):
    bot.add_cog(Fun(bot))