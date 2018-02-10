import discord
from discord.ext import commands
import asyncio
import pickle
import random
import io
import os
import sys
import traceback
import textwrap
from contextlib import redirect_stdout

bot = commands.Bot(command_prefix="$", description="A simple bot created in discord.py library by Nyan Pikachu#4148 for moderation and misc commands!", owner_id=279974491071709194)

bot.load_extension("cogs.info")
bot.load_extension("cogs.mod")

#eval!!!
def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')

bot.load_extension("cogs.info")
bot.load_extension("cogs.mod")

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
                


#normal commands.ill put into cogs later
@bot.event
async def on_ready():
    print("Bot is online!")
    await bot.change_presence(game=discord.Game(name=f"over {len(bot.guilds)} Guilds! | $help", type=3))
    
@bot.command()
async def say(ctx, *, msg: str):
    """owner only command- print a message"""
    await ctx.message.delete()
    await ctx.send(msg)
    
@bot.command()
async def coinflip(ctx):
    """Flips a coin!"""
    flip = random.choice(["Heads", "Tails"])
    await ctx.send(flip)
    
@bot.command()
async def hug(ctx, user: discord.Member=None):
   """hugs a user"""
   if not user:
      await ctx.send(f"Please mention someone for this command to work {ctx.author.mention}" )
   embed = discord.Embed(title="Hug!".format(user.name), description= f"{ctx.author} has sent {user} a hug !", color=0xffb6c1)
   embed.set_thumbnail(url=user.avatar_url)
   await ctx.send(embed=embed)
    
bot.run(os.environ.get("TOKEN"))
