import discord
from discord.ext import commands
import asyncio
import pickle
import random
import io
import os
import sys
import traceback
import datetime
import textwrap
from contextlib import redirect_stdout

bot = commands.Bot(command_prefix="$", description="A simple bot created in discord.py library by Nyan Pikachu#4148 for moderation and misc commands!", owner_id=279974491071709194)

def dev_check(id):
    with open('data/devlist.json') as f:
        devs = json.load(f)
    if id in devs:
        return True
    return False

bot.load_extension("cogs.info")
bot.load_extension("cogs.mod")
bot.load_extension("cogs.misc")

#eval!!!
def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')

devs = [
    279974491071709194
]

@bot.command()
@commands.is_owner()
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
                
@bot.event
async def on_ready():
    print("Bot is online!")
    await bot.change_presence(game=discord.Game(name=f"over {len(bot.guilds)} Guilds! | $help", type=3))
    
@commands.command(name='presence', hidden=True)
async def _presence(self, ctx, type=None, *, game=None):
    '''Change the bot's presence'''
    if not dev_check(ctx.author.id):
        return
    
    if type is None:
        await ctx.send(f'Usage: `{ctx.prefix}presence [game/stream/watch/listen] [message]`')
    else:
        if type.lower() == 'stream':
            await self.bot.change_presence(game=discord.Game(name=game, type=1, url='https://www.twitch.tv/a'), status='online')
            await ctx.send(f'Set presence to. `Streaming {game}`')
        elif type.lower() == 'game':
            await self.bot.change_presence(game=discord.Game(name=game))
            await ctx.send(f'Set presence to `Playing {game}`')
        elif type.lower() == 'watch':
            await self.bot.change_presence(game=discord.Game(name=game, type=3), afk=True)
            await ctx.send(f'Set presence to `Watching {game}`')
        elif type.lower() == 'listen':
            await self.bot.change_presence(game=discord.Game(name=game, type=2), afk=True)
            await ctx.send(f'Set presence to `Listening to {game}`')
        elif type.lower() == 'clear':
            await self.bot.change_presence(game=None)
            await ctx.send('Cleared Presence')
        else:
            await ctx.send('Usage: `.presence [game/stream/watch/listen] [message]`')
 

bot.run(os.environ.get("TOKEN"))
