import discord
from discord.ext import commands
import random
import io
import os
import sys
import traceback
import datetime
import pynite
import textwrap
from contextlib import redirect_stdout
from ext import utility
import asyncio
import json
from motor import motor_asyncio

dbclient = motor_asyncio.AsyncIOMotorClient('mongodb://PikaBot:' + os.environ.get('DBPASS') + '@ds163711.mlab.com:63711/pikabot')
db = dbclient.pikabot

async def get_pre(bot, message):
    try:
        result = await db.settings.find_one({'_id': str(message.guild.id)})
    except AttributeError:
        return ["P.", "p.", f"{bot.user.mention} "]
    if not result or not result.get('prefix'):
        return ["P.", "p.", f"{bot.user.mention} "]
    return result['prefix']

bot = commands.Bot(command_prefix=get_pre, description="A simple bot created in discord.py library by Nyan Pikachu#4148 for moderation and misc commands!", owner_id=279974491071709194)


devs = [
    279974491071709194,
    199436790581559296
]

bot.load_extension("cogs.info")
bot.load_extension("cogs.mod")
bot.load_extension("cogs.misc")
bot.load_extension("cogs.fortnite")
bot.load_extension("cogs.pokedex")
bot.load_extension("cogs.cr")

#eval!!!
def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')

@bot.command()
@utility.developer()
async def eval(ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
        }
        
        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                await ctx.send(f'```py\n{value}{ret}\n```')            

#events                
@bot.event
async def on_ready():
    print("Bot is online!")
    await bot.change_presence(activity=discord.Activity(name=f'{len(bot.guilds)} servers! | p.help', type=discord.ActivityType.streaming))
    x = bot.get_channel(424677910314745856)
    now = datetime.datetime.utcnow()
    em = discord.Embed(color=discord.Color.gold())
    em.title = bot.user.name
    em.description = 'bot is online!'
    em.add_field(name='User ID:', value=bot.user.id)
    em.add_field(name='Started at:', value=now.strftime("%A, %d. %B %Y %I:%M%p"))
    await x.send(embed=em)

@bot.event
async def on_guild_join(guild):
    x = bot.get_channel(424677910314745856)
    now = datetime.datetime.utcnow()
    em = discord.Embed(color=discord.Color.green())
    em.title = bot.user.name
    em.description = 'Guild added'
    em.add_field(name='Guild Name:', value=guild.name)
    em.add_field(name='Guild id:', value=guild.id)
    em.add_field(name='Joined at:', value=now.strftime("%A, %d. %B %Y %I:%M%p"))
    await x.send(embed=em)

@bot.event
async def on_guild_remove(guild):
    x = bot.get_channel(424677910314745856)
    now = datetime.datetime.utcnow()
    em = discord.Embed(color=discord.Color.red())
    em.title = bot.user.name
    em.description = 'Guild removed'
    em.add_field(name='Guild Name:', value=guild.name)
    em.add_field(name='Guild id:', value=guild.id)
    em.add_field(name='Left at:', value=now.strftime("%A, %d. %B %Y %I:%M%p"))
    await x.send(embed=em)

#commands
@bot.command()
async def ping(ctx):
    '''Pong! Get the bot's response time'''
    em = discord.Embed(color=discord.Color.gold())
    em.title = "Pong!"
    em.description = f'{bot.latency * 1000:.0f} ms'
    await ctx.send(embed=em)

@bot.command(name='presence')
@utility.developer()
async def _presence(ctx, type=None, *, game=None):
    '''Change the bot's presence'''
    if type is None:
        await ctx.send(f'Usage: `{ctx.prefix}presence [game/stream/watch/listen] [message]`')
    else:
        if type.lower() == 'stream':
            await bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.streaming))
            await ctx.send(f'Set presence to. `Streaming {game}`')
        elif type.lower() == 'game':
            await bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.playing))
            await ctx.send(f'Set presence to `Playing {game}`')
        elif type.lower() == 'watch':
            await bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.watching))
            await ctx.send(f'Set presence to `Watching {game}`')
        elif type.lower() == 'listen':
            await bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.listening))
            await ctx.send(f'Set presence to `Listening to {game}`')
        elif type.lower() == 'clear':
            await bot.change_presence(activity=discord.Activity(name=None))
            await ctx.send('Cleared Presence')
        else:
            await ctx.send('Usage: `.presence [game/stream/watch/listen] [message]`')
 

bot.run(os.environ.get('TOKEN'))
