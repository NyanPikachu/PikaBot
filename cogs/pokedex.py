import discord
from discord.ext import commands
from pokedex import pokedex
pokedex = pokedex.Pokedex()

class Pokedex:
    '''Pokemon info related commands!'''
    def __init__(self, bot):
        self.bot = bot
           
    @commands.command()
    async def pokemon(self, ctx, poke: str=None):
        '''Get A Pokemon's info!'''
        pokemon = pokedex.get_pokemon_by_name(poke)
        em = discord.Embed(name=pokemon[0]['name'] + "'s info!")
        em.set_author(name=ctx.author.name)
        em.add_field(name='Species', value=pokemon[0]['species'])
        em.add_field(name='Number', value=pokemon[0]['number'])
        em.add_field(name='Types', value=pokemon[0]['types'])
        em.add_field(name=' Normal Abilities', value=pokemon[0]['abilities']['normal'])
        em.add_field(name='Hidden Abilities', value=pokemon[0]['abilities']['hidden'])
        em.add_field(name='Height', value=pokemon[0]['height'])
        em.add_field(name='Weight', value=pokemon[0]['weight'])
        em.add_field(name='Evolutions', value=pokemon[0]['family']['evolutionLine'])
        em.set_thumbnail(url=pokemon[0]['sprite'])
        em.set_footer(text="Pika Bot | scripted in discord.py")
        await ctx.send(embed=em)
    
def setup(bot):
    bot.add_cog(Pokedex(bot))
