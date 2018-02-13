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

def load_json(path, key):
    with open(f'.data{path}') as f:
        config = json.load(f)
    return config.get(key)

def dev_check(id):
    with open('data/devlist.json') as f:
        devs = json.load(f)
    if id in devs:
        return True
    return False

def fomat_command_help(ctx, cmd):
    '''Format help for a command'''
    color = discord.Color.gold()
    em = discord.Embed(color=color, description=cmd.help)
    
    if hasattr(cmd, 'invoke_without_command') and cmd.invoke_without_command:
        em.title = f'`Usage: {ctx.prefix}{cmd.signature}`'
    else:
        em.title = f'{ctx.prefix}{cmd.signature}'
        
    return em

async def send_cmd_help(ctx):
    cmd = ctx.command
    em = discord.Embed(title=f'Usage: {ctx.prefix + cmd.signature}')
    em.color = discord.Color.green()
    em.description = cmd.help
    return em

def format_cog_help(ctx, cog):
    '''Format help for a cog'''
    signatures = []
    color = discord.Color.green()
    em = discord.Embed(color=color, description=f'*{inspect.getdoc(cog)}*')
    em.title = type(cog).__name__.replace('_', ' ')
    cc = []
    for cmd in bot.commands:
        if not cmd.hidden:
            if cmd.instance is cog:
                cc.append(cmd)
                signatures.append(len(cmd.name) + len(ctx.prefix))
    max_length = max(signatures)
    abc = sorted(cc, key=lambda x: x.name)
    cmds = ''
    for c in abc:
        cmds += f'`{ctx.prefix + c.name:<{max_length}} '
        cmds += f'{c.short_doc:<{max_length}}`\n'
    em.add_field(name='Commands', value=cmds)
 
    return em
 
 
def format_bot_help(ctx):
    signatures = []
    fmt = ''
    commands = []
    for cmd in bot.commands:
        if not cmd.hidden:
            if type(cmd.instance).__name__ == 'NoneType':
                commands.append(cmd)
                signatures.append(len(cmd.name) + len(ctx.prefix))
    max_length = max(signatures)
    abc = sorted(commands, key=lambda x: x.name)
    for c in abc:
        fmt += f'`{ctx.prefix + c.name:<{max_length}} '
        fmt += f'{c.short_doc:<{max_length}}`\n'
    em = discord.Embed(title='Bot', color=discord.Color.green())
    em.description = '*Commands for the main bot.*'
    em.add_field(name='Commands', value=fmt)
 
    return em
 

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

bot.remove_command('help')              
                
@bot.event
async def on_ready():
    print("Bot is online!")
    await bot.change_presence(game=discord.Game(name=f"over {len(bot.guilds)} Guilds! | $help", type=3))

@bot.command()
async def help(ctx, *, command: str=None):
    '''Shows this message'''
    
    if command is none:
        aliases = {
            'info': 'Info commands',
            'misc': 'Miscellaneous commands',
            'mod': 'Moderation commands'
        }
        
        if command.lower() in aliases.keys():
            command = aliases[command]
            
        cog = bot.get_cog(command.replace(' ', '_').title())
        cmd = bot.get_command(command)
        if cog is not None:
            em = format_cog_help(ctx, cog)
        elif cmd is not None:
            em = format_command_help(ctx, cmd)
        else:
            await ctx.send('No command found.')
        return await ctx.send(embed=em)
    
    pages = []
    for cog in bot.cogs.values():
        em = format_cog_help(ctx, cog)
        pages.append(em)
    em = format_bot_help(ctx)
    pages.append(em)
    
    p_session = PaginatorSession(ctx, footer=f'Type {ctx.prefix}help command for more info on a command.', pages=pages)
    await p_session.run()
    
@bot.command(name='presence', hidden=True)
async def _presence(self, ctx, type=None, *, game=None):
    '''Change the bot's presence'''
    if not dev_check(ctx.author.id):
        return
    
    if type is None:
        await ctx.send(f'Usage: `{ctx.prefix}presence [game/stream/watch/listen] [message]`')
    else:
        if type.lower() == 'stream':
            await self.bot.change_presence(game=discord.Game(name=f"{game}", type=1, url='https://www.twitch.tv/a'), status='online')
            await ctx.send(f'Set presence to. `Streaming {game}`')
        elif type.lower() == 'game':
            await self.bot.change_presence(game=discord.Game(name=f"{game}"))
            await ctx.send(f'Set presence to `Playing {game}`')
        elif type.lower() == 'watch':
            await self.bot.change_presence(game=discord.Game(name=f"{game}", type=3), afk=True)
            await ctx.send(f'Set presence to `Watching {game}`')
        elif type.lower() == 'listen':
            await self.bot.change_presence(game=discord.Game(name=f"{game}", type=2), afk=True)
            await ctx.send(f'Set presence to `Listening to {game}`')
        elif type.lower() == 'clear':
            await self.bot.change_presence(game=None)
            await ctx.send('Cleared Presence')
        else:
            await ctx.send('Usage: `.presence [game/stream/watch/listen] [message]`')
 

bot.run(os.environ.get("TOKEN"))
